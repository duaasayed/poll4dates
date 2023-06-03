from typing import Any
from django.db.models.query import QuerySet
from .models import Poll
from django.views.generic import ListView

class PollList(ListView):
    model = Poll
    context_object_name = 'polls'
    template_name='polls/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        current_user = self.request.user
        queryset = Poll.objects.select_related('event').filter(user=current_user)
        return queryset
