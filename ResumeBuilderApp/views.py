from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, Resume
import json
from django.http import JsonResponse
from django.core.files.base import ContentFile


def home(request):
    return render(request, 'pages/home.html')


def dashboard(request):
    return render(request, 'pages/Dashboard.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password is incorrect.')
            return render(request, 'pages/login.html')
    # GET request should render login page without any context data
    return render(request, 'pages/login.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            if user is not None:
              messages.success(request, 'Account was created for ' + user)
            else:
              messages.error(request, 'Account was not created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'pages/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')

def edit_user(request, user_id): # User editing
  user = User.objects.get(id=user_id)
  if request.method == 'POST':
    form = UserEditForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        return render(request, 'pages/Dashboard.html')  # Redirect to dashboard after editing
  else:
    form = UserEditForm(instance=user)
  return render(request, 'pages/edit_user.html', {'form': form})

def editor(request):
    context = {}
    return render(request, 'pages/editor.html', context)

#function to save resume
def saveResume(request):
  if request.method == 'POST':
    content = request.POST.get('data', 'Hello World!')
    print(content)
    #if we want to check resume contents for security reasons

    #saves resume to database
    username = request.user
    user = User.objects.get(email=username)
    resumeCount = Resume.objects.filter(user=user).count()
    resume = Resume(name= "Resume" + str(resumeCount), user=user, resume_file=content)
    resume.save()
    return redirect('editor')
  else:
    return redirect('editor')