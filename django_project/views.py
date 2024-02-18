from django.shortcuts import render

def login_view(request):
    return render(request, 'pages/login.html')

def register_view(request):
    return render(request, 'pages/register.html')