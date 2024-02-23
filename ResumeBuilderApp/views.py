from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import MyUserCreationForm, MyAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = MyAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = MyAuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        print("Register view function is being executed!")
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()
    return render(request, 'pages/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('pages/login.html')


def home(request):
    return render(request, 'pages/home.html')
