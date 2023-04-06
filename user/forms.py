from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class AuthenticationForms(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'phonenumber', 'password')
