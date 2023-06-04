from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'polls'

urlpatterns = [
    path("", TemplateView.as_view(template_name='polls/index.html'), name='index'),
    path("plan/", views.PollCreate.as_view(), name='plan'),
    path("polls/", views.PollList.as_view(), name='my_polls'),
    path("polls/<int:pk>/", views.PollDetail.as_view(), name='poll_detail'),
    path("polls/<int:pk>/edit/", views.PollUpdate.as_view(), name='poll_update')
]