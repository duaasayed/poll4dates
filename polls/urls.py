from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'polls'

urlpatterns = [
    path("", TemplateView.as_view(template_name='polls/index.html'), name='index'),
    path("plan/", views.PollCreate.as_view(), name='plan'),
    path("polls/", views.PollList.as_view(), name='my_polls'),
    path("polls/<int:pk>/", views.PollDetail.as_view(), name='poll_detail'),
    path("polls/<int:pk>/edit/", views.PollUpdate.as_view(), name='poll_update'),
    path("polls/<int:pk>/delete/", views.PollDelete.as_view(), name='delete'),
    path("polls/<int:pk>/invite/", views.invite, name='invite'),
    path("polls/<int:pk>/guests/", views.add_guest, name='add_guest'),
    path("polls/<int:poll_pk>/guests/<int:guest_pk>/", views.get_guest, name='get_guest'),
    path("polls/<int:poll_pk>/guests/<int:guest_pk>/vote/", views.vote, name='vote'),
]
