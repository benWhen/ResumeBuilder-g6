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

class EducationForm(forms.ModelForm):
  class Meta:
    model = Education
    fields = ['institution_name', 'degree', 'major', 'start_date', 'end_date']
