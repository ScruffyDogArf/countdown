import string
import random
import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from countdown_model.models import Countdown, CountdownForm

# Create your views here.
def index(request):
    return render(request, 'countdown/index.html')

def get_countdowns(user):
    countdowns = Countdown.objects.filter(user=user)
    return countdowns

def get_countdowns_api(request):
    response = {'status': None, 'error': None, 'response': None}
    username = request.user
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type="application/json")
    countdowns =  get_countdowns(user=user)
    response2 = []
    for countdown in countdowns:
        response2 += [json.loads(countdown.json())]
    response['response'] = response2
    response['status'] = 200
    return HttpResponse(json.dumps(response), content_type="application/json")

def create_countdown(request):
    response = {'status': None, 'error': None, 'response': None}
    username = request.user
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        countdown = Countdown(user=user)
        form = CountdownForm(request.POST, request.FILES, instance=countdown)
        countdown = form.save()
        countdown.id_string = '{}'.format(countdown.id)
        countdown.id_string += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        countdown.save()
        response['status'] = 200
        response['response'] = json.loads(countdown.json())
    except ValueError as e:
        response['status'] = 400
        response['error'] = str(e) + '\n{}'.format(form.errors)
        return HttpResponse(json.dumps(response), content_type="application/json")
    return HttpResponse(json.dumps(response), content_type="application/json")

def update_countdown(request, id_string):
    username = request.user
    response = {'status': None, 'error': None, 'response': None}
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        countdown = Countdown.objects.get(id_string=id_string)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'Countdown not found, id_string: {}'.format(id_string)
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        form = CountdownForm(request.POST, instance=countdown)
        form.save()
        response['status'] = 200
        response['response'] = json.loads(countdown.json())
        return HttpResponse(json.dumps(response), content_type='application/json')
    except ValueError as e:
        response['status'] = 400
        response['error'] = str(e)
        return HttpResponse(json.dumps(response), content_type='application/json')
    except Exception as e:
        response['status'] = 400
        response['error'] = str(e)
        return HttpResponse(json.dumps(response), content_type='application/json')
        

def delete_countdown(request, id_string):
    response = {'status': None, 'error': None, 'response': None}
    username = request.user
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type="application/json")
    try:
        countdown = Countdown.objects.get(id_string=id_string)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'Countdown not found, Id: {}'.format(id_string)
        return HttpResponse(json.dumps(response), content_type="application/json")
    if countdown.user != user:
        response['status'] = 400
        response['error'] = 'Unauthorised request, username: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type="application/json")
    countdown.delete()
    response['status'] = 200
    return HttpResponse(json.dumps(response), content_type="application/json")
