from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'polls'

urlpatterns = [
    path("", TemplateView.as_view(template_name='polls/index.html'), name='index'),
    path("polls/", views.PollList.as_view(), name='my_polls'),
]
