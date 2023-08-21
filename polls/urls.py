from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'polls'

urlpatterns = [
    path("", TemplateView.as_view(template_name='polls/index.html'), name='index'),
    path("plan/", views.PollCreate.as_view(), name='plan'),
    path("polls/", views.PollList.as_view(), name='my_polls'),
    path("polls/<uuid:guid>/", views.PollDetail.as_view(), name='poll_detail'),
    path("polls/<uuid:guid>/edit/", views.PollUpdate.as_view(), name='poll_update'),
    path("polls/<uuid:guid>/delete/", views.PollDelete.as_view(), name='delete'),
    path("polls/<uuid:guid>/invite/", views.invite, name='invite'),
    path("polls/<uuid:guid>/guests/", views.add_guest, name='add_guest'),
    path("polls/<uuid:poll_guid>/guests/<uuid:guest_guid>/", views.get_guest, name='get_guest'),
    path("guests/<uuid:guid>/edit/", views.edit_guest_name, name="edit_guest_name"),
    path("contact/", views.contact, name='contact')
]
