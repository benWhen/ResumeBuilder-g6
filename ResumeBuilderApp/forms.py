from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 150:
            raise ValidationError('Username should not exceed 150 characters.')
        elif not username.isalnum():
            raise ValidationError('Username can only contain letters, numbers, and underscores')
        return username
