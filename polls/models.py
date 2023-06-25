from django.db import models
from django.utils import timezone
import string
import secrets 

def generate_token(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join([secrets.choice(alphabet) for i in range(length)])


class Poll(models.Model):
    creator = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='polls')
    event_name = models.CharField(max_length=225)
    event_organizer = models.CharField(max_length=225)
    event_location = models.CharField(max_length=225, blank=True, null=True)
    event_details = models.CharField(max_length=350, blank=True, null=True)
    event_timezone = models.CharField(max_length=225)
    rsvp_by = models.DateTimeField()
    token = models.CharField(max_length=8, default=generate_token(8))

    def __str__(self):
        return self.event_name
    
    @property
    def ended(self):
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


class TimeSlot(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='time_slots')
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    @property
    def votes_count(self):
        return self.votes.count()

class Guest(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='votes')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='votes')
    

class Message(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']
