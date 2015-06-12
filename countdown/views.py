import django
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):
    username = request.user
    # try:
    #     user = User.objects.get(username=username)
    #     authenticated = user.authenticate()
    #     if authenticated:
    #         return render(request, 'django_project/home.html')
    #     else:
    #         return render(request, 'django_project/index.html')
    # except ObjectDoesNotExist:
    return render(request, 'django_project/index.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = django.contrib.auth.authenticate(username=username, password=password)
    if user:
        django.contrib.auth.login(request, user)
        return redirect('/home')
    else:
        return render(request, 'django_project/index.html')

def home(request):
    username = request.user
    return render(request, 'django_project/home.html', {'username': username})

#     print 'hello'
    # form = UserLoginForm(request)
    # form.authorize()
    # if form.isokay:
    #     return render(request, 'django_project/home.html')
    # else:
    #     return 
