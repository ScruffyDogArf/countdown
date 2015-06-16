import datetime
import django
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from countdown_model.models import Countdown, CountdownForm
from countdown_model.views import get_countdowns

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
    countdowns = get_countdowns(request, json=False)
    for countdown in countdowns:
        countdown.update_state()
    return render(request, 'countdown/home.html', {'username': username, 'new_countdown_form': CountdownForm(), 'countdowns': countdowns})

