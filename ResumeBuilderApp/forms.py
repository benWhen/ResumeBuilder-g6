from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class UserEditForm(forms.ModelForm): #comment so I can re-push
  class Meta:
      model = User
      fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
