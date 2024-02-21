from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email',)  # Adjust fields as needed

class MyAuthenticationForm(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')