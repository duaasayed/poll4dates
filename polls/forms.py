from typing import Any
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Poll
from datetime import datetime
import ast

class TimeSlotsField(forms.CharField):
    widget = forms.SelectMultiple()

    def clean(self, value: Any) -> Any:
        value = super().clean(value)
        if not value:
            raise ValidationError('This field is required')
        timeslots = []
        value = ast.literal_eval(value)
        for slot in value:
            day, start_time, end_time = slot.split(',')
            start_time = datetime.strptime(start_time, '%H:%M')
            end_time = datetime.strptime(end_time, '%H:%M')
            timeslots.append({'day': day, 'start': start_time, 'end': end_time})
        return timeslots

class PollCreationForm(forms.Form):
    event_name = forms.CharField(max_length=225, label='Name the Event *')
    event_organizer = forms.CharField(max_length=225, label='Event Organizer *')
    event_details = forms.CharField(max_length=350, label='Event details (optional)', required=False)
    event_location = forms.CharField(max_length=225, label='Event location (optional)', required=False)
    event_timezone = forms.CharField(max_length=225, label='Event time zone')
    rsvp_by = forms.DateTimeField(label='RSVP by *')
    timeslots = TimeSlotsField(label='Timeslots')

    def clean_rsvp_by(self):
        rsvp_by = self.cleaned_data.get('rsvp_by')
        if rsvp_by < timezone.now():
            raise ValidationError('Please enter a future date.')
        return rsvp_by

    def save(self, *args, **kwargs):
        data = {k:v for k,v in self.cleaned_data.items() if k != 'timeslots'}
        poll = Poll(**data)
        return poll

