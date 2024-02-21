from django.shortcuts import render, redirect
from .forms import MyUserCreationForm, MyAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.views import View
User = get_user_model()

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pages/register.html')
    else:
        form = MyUserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = MyAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pages/register.html')
    else:
        form = MyAuthenticationForm()
    return render(request, 'pages/login.html', {'form' : form})

def user_logout(request):
    logout(request)
    return redirect('pages/register.html')

def home(request):
    return render(request, 'pages/register.html')