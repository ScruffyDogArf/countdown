import string
import random
import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from countdown.models import Countdown

# Create your views here.
def index(request):
    return render(request, 'countdown/index.html')

def get_countdowns(request):
    response = {'status': None, 'error': None, 'response': None}
    username = request.user
    try:
        user = User.objects.get(username=username)
        countdowns = Countdown.objects.filter(user=user)
        response['response'] = json.loads(serializers.serialize("json", countdowns))
        response['status'] = 200
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
    return HttpResponse(json.dumps(response), content_type="application/json")

def create_countdown(request):
    response = {'status': None, 'error': None, 'response': None}
    username = request.user
    post = request.GET # TODO: Change to POST later, this is only for testing purposes
    try:
        title = post['title']
    except MultiValueDictKeyError:
        response['status'] = 400
        response['error'] = 'Missing required argument: title'
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        brief_description = post['description']
    except MultiValueDictKeyError:
        response['status'] = 400
        response['error'] = 'Missing required argument: description'
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        end_datetime = datetime.datetime.strptime(post['end-datetime'], '%Y-%m-%d-%H-%M-%S')
    except MultiValueDictKeyError:
        response['status'] = 400
        response['error'] = 'Missing required argument: end-datetime'
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        image = post['image']
    except MultiValueDictKeyError:
        image = None
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type='application/json')
    countdown = Countdown()
    countdown.user = user
    countdown.title = title
    countdown.brief_description = brief_description
    countdown.end_datetime = end_datetime
    countdown.image = image
    countdown.save()
    countdown.id_string = '{}'.format(countdown.id)
    countdown.id_string += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    countdown.save()
    response['status'] = 200
    response['response'] = json.loads(serializers.serialize("json", [countdown]))[0]
    return HttpResponse(json.dumps(response), content_type="application/json")

def update_countdown(request):
    username = request.user
    response = {'status': None, 'error': None, 'response': None}
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type='application/json')
    post = request.GET # TODO: GET -> POST
    try:
        id_string = post['id-string']
    except MultiValueDictKeyError:
        response['status'] = 400
        response['error'] = 'Missing required argument: id-string'
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        countdown = Countdown.objects.get(id_string=id_string)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'Countdown not found: id-string: {}'.format(id_string)
        return HttpResponse(json.dumps(response), content_type='application/json')
    if countdown.user != user:
        response['status'] = 400
        response['error'] = 'Unauthorised request: username: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        try:
            end_datetime = datetime.datetime.strptime(post['end-datetime'], '%Y-%m-%d-%H-%M-%S')
            countdown.end_datetime = end_datetime
        except MultiValueDictKeyError:
            pass
        try:
            title = post['title']
            countdown.title = title
        except MultiValueDictKeyError:
            pass
        try:
            brief_description = post['description']
            countdown.brief_description = brief_description
        except MultiValueDictKeyError:
            pass
        try:
            image = post['image']
            countdown.image = image
        except MultiValueDictKeyError:
            pass
        countdown.save()
        response['status'] = 200
        response['response'] = json.loads(serializers.serialize("json", [countdown]))[0]
    return HttpResponse(json.dumps(response), content_type="application/json")

def delete_countdown(request):
    response = {'status': None, 'error': None, 'response': None}
    username = request.user
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type="application/json")
    try:
        id_string = request.GET['id-string'] # TODO: change this to POST, using GET for testing
        countdown = Countdown.objects.get(id_string=id_string)
    except MultiValueDictKeyError:
        response['status'] = 400
        response['error'] = 'Missing required argument: id-string'
        return HttpResponse(json.dumps(response), content_type="application/json")
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
