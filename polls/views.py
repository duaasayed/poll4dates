from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from .models import Poll
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .forms import PollCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone

class PollCreate(FormView):
    template_name = 'polls/create.html'
    form_class = PollCreationForm

    def form_valid(self, form: Any) -> HttpResponse:
        poll = form.save()
        poll.creator = self.request.user
        poll.save()
        for slot in form.cleaned_data['timeslots']:
            poll.time_slots.create(**slot)
        success_url = reverse_lazy('polls:poll_detail', kwargs={'pk': poll.pk})
        return redirect(success_url, {'poll': poll})


class PollList(ListView):
    model = Poll
    context_object_name = 'polls'
    template_name='polls/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        current_user = self.request.user
        queryset = Poll.objects.filter(creator=current_user)
        return queryset
    

class PollDetail(DetailView):
    model = Poll
    template_name='polls/show.html'
    context_object_name = 'poll'


class PollUpdate(UpdateView):
    model = Poll
    template_name = "polls/show.html"
    fields = ['event_name', 'event_details', 'event_location', 'rsvp_by']

    def post(self, *args: str, **kwargs: Any) -> HttpResponse:
        post_data = self.request.POST

        if '_method' in post_data and post_data['_method'] == 'put':
            data = {k:v for k,v in post_data.items() if k not in ['csrfmiddlewaretoken', '_method']}
            
            poll = Poll.objects.get(pk=self.get_object().pk)
            
            for field, value in data.items():
                setattr(poll, field, value)
                poll.save()

            if 'close' in data:
                data['rsvp_by'] = timezone.now()
            
            if 'date' in data:
                poll.time_slots.create(day=data['date'], start=data['start'], end=data['end'])

            if 'timeslots[]' in data:
                timeslots = post_data.getlist('timeslots[]')
                for slot in timeslots:
                    poll.time_slots.get(pk=slot).delete()
              
        success_url = reverse_lazy('polls:poll_detail', kwargs={'pk': poll.pk})
        return redirect(success_url, {'poll': poll})
    

class PollDelete(DeleteView):
    model = Poll
    success_url = reverse_lazy('polls:my_polls')