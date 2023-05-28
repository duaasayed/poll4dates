from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.Registration.as_view(), name="register"),
    path("", include("django.contrib.auth.urls")),
]
