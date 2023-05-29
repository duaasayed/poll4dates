from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignUpForm

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=225, label='Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autofocus': True})

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data.get('name')
        user.save()
        return user
    

class CustomSocialSignupForm(SocialSignUpForm):
    name = forms.CharField(max_length=225, label='Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autofocus': True})

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data.get('name')
        user.save()
        return user
