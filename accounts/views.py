from django.views.generic.edit import FormView
from .forms import RegistrationForm
from django.urls import reverse_lazy
from .models import User


class Registration(FormView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        data = form.cleaned_data
        User.objects.create_user(data["name"], data["email"], data["password1"])
        return super().form_valid(form)


