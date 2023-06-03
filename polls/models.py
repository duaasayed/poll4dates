from django.db import models

class Event(models.Model):
    organizer = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=350)
    location = models.CharField(max_length=225)
    time_zone = models.CharField(max_length=225)
    

class Poll(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='polls')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rsvp_by = models.DateTimeField()

    def __str__(self):
        return self.event.name


class TimeSlot(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='time_slots')
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()


class Vote(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='votes')
    guest_name = models.CharField(max_length=225)
    guest_email = models.EmailField(blank=True, null=True)
    