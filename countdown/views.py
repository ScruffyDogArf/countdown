import django
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):
    username = request.user
    return render(request, 'countdown/index.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = django.contrib.auth.authenticate(username=username, password=password)
    if user:
        django.contrib.auth.login(request, user)
        return redirect('/home')
    else:
        return render(request, 'countdown/index.html')

def home(request):
    username = request.user
    return render(request, 'countdown/home.html', {'username': username})

