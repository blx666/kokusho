
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):
    number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)