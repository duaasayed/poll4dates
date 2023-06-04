from django.db import models
from django.utils import timezone
    

class Poll(models.Model):
    creator = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='polls')
    event_name = models.CharField(max_length=225)
    event_organizer = models.CharField(max_length=225)
    event_location = models.CharField(max_length=225, blank=True, null=True)
    event_details = models.CharField(max_length=350, blank=True, null=True)
    event_timezone = models.CharField(max_length=225)
    rsvp_by = models.DateTimeField()

    def __str__(self):
        return self.event_name
    
    @property
    def ended(self):
        return self.rsvp_by < timezone.now()


class TimeSlot(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='time_slots')
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()


class Vote(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='votes')
    guest_name = models.CharField(max_length=225)
    guest_email = models.EmailField(blank=True, null=True)
    