from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from .models import Poll
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .forms import PollCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy

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
        queryset = Poll.objects.select_related('event').filter(user=current_user)
        return queryset
