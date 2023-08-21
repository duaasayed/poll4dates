from django.db import models
from django.utils import timezone
import string
import secrets 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.db.models.constraints import UniqueConstraint
from datetime import datetime, timedelta
from django.db import transaction
import pytz
from django.urls import reverse
import uuid


def generate_token(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join([secrets.choice(alphabet) for i in range(length)])


def str_to_date(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M')


class Poll(models.Model):
    guid = models.UUIDField(default=uuid.uuid1, db_index=True) 
    creator = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='polls')
    event_name = models.CharField(max_length=225)
    event_organizer = models.CharField(max_length=225)
    event_location = models.CharField(max_length=225, blank=True, null=True)
    event_details = models.CharField(max_length=350, blank=True, null=True)
    event_timezone = models.CharField(max_length=225)
    rsvp_by = models.DateTimeField()
    token = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.event_name


    def get_absolute_url(self):
        return reverse("polls:poll_detail", kwargs={"pk": self.pk})
    
    
    @property
    def ended(self):
        if isinstance(self.rsvp_by, str):
            return str_to_date(self.rsvp_by) < datetime.now()
        return self.rsvp_by < timezone.now()
    
    @property
    def max_vote(self):
        return self.time_slots.annotate(votes_count=models.Count('votes'))\
            .aggregate(max_vote=models.Max('votes_count'))['max_vote']
    
    @property
    def guests_voted(self):
        return self.guests.filter(votes__isnull=False).distinct()
    
    @property
    def guests_waiting(self):
        return self.guests.filter(votes__isnull=True)


    def save(self, *args, **kwargs):
        self.token = generate_token(8)

        super().save(*args, **kwargs)

        rsvp_by = None

        if isinstance(self.rsvp_by, str):
            rsvp_by = str_to_date(self.rsvp_by)

        else:
            desired_tz = pytz.timezone("Africa/Cairo")
            rsvp_by = self.rsvp_by.astimezone(desired_tz)


        task_found = PeriodicTask.objects.filter(name__contains=self.pk).exists()
        
        with transaction.atomic() :
            if task_found:
                task = PeriodicTask.objects.get(name__contains=self.pk)
                
                desired_tz = pytz.timezone("Africa/Cairo")
                converted_time = task.clocked.clocked_time.astimezone(desired_tz)
                t1 = converted_time.strftime("%Y-%m-%dT%H:%M")
                
                rsvp_plus = rsvp_by + timedelta(minutes=2)
                t2 = rsvp_plus.strftime("%Y-%m-%dT%H:%M")
                
                if t1 != t2:
                    task.clocked.delete()
                    task.delete()

                    clocked_schedule = ClockedSchedule.objects.create(clocked_time=rsvp_by + timedelta(minutes=2))

                    PeriodicTask.objects.create(
                        clocked=clocked_schedule,
                        name=f'Send result email to poll {self.id} creator and guests',
                        task='polls.tasks.fetch_result_and_send_email',
                        args=[self.id],
                        one_off=True
                    )
            else:
                clocked_schedule = ClockedSchedule.objects.create(clocked_time=rsvp_by + timedelta(minutes=2))

                PeriodicTask.objects.create(
                    clocked=clocked_schedule,
                    name=f'Send result email to poll {self.id} creator and guests',
                    task='polls.tasks.fetch_result_and_send_email',
                    args=[self.id],
                    one_off=True
                )

class TimeSlot(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='time_slots')
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f'{self.day}@{self.start}-{self.end}'

    @property
    def votes_count(self):
        return self.votes.count()

class Guest(models.Model):
    guid = models.UUIDField(default=uuid.uuid1, db_index=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=250, blank=False, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint("poll", "name", name="unique_name_per_poll"),
            UniqueConstraint("poll", "email", name="unique_email_per_poll")
        ]


class Vote(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='votes')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='votes')
    

class Message(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='messages')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    sender_id = models.BigIntegerField()
    content_sender = GenericForeignKey('content_type', 'sender_id')
    content = models.CharField(max_length=250)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    