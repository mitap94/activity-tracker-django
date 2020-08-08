from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.models import User


class SignUpForm(UserCreationForm):
    """Signup form based on the custom user model"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'gender', 'password1', 'password2', )
