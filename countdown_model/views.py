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

def get_countdowns(request):
    response = {'status': None, 'error': None, 'response': None}
    username = request.user
    try:
        user = User.objects.get(username=username)
        countdowns = Countdown.objects.filter(user=user)
        response2 = []
        for countdown in countdowns:
            x = {} # countdown attributes to return
            x['title'] = countdown.title
            x['description'] = countdown.brief_description
            x['end_datetime'] = countdown.end_datetime.isoformat() + 'Z'
            x['id_string'] = countdown.id_string
            try:
                x['image'] = countdown.image.url
            except ValueError:
                x['image'] = None
            response2.append(x)
        response['response'] = response2
        response['status'] = 200
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
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
        print 'request.POST: {}'.format(request.POST)
        print 'request.FILES: {}'.format(request.FILES)
        form = CountdownForm(request.POST, request.FILES, instance=countdown)
        countdown = form.save()
        print 'form.data: {}'.format(form.data)
        countdown.id_string = '{}'.format(countdown.id)
        countdown.id_string += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        countdown.save()
    except ValueError as e:
        response['status'] = 400
        response['error'] = str(e) + '\n{}'.format(form.errors)
        return HttpResponse(json.dumps(response), content_type="application/json")
    return HttpResponse(countdown.json(), content_type="json")

        # response['status'] = 200
        # response2 = {}
        # response2['title'] = countdown.title
        # response2['brief_description'] = countdown.brief_description
        # response2['end_date'] = countdown.end_date
        # response2['end_time'] = countdown.end_time
        # response2['days']
        # response2['hours']
        # response2['minutes']
        # response2['seconds']
        # response2['complete']
        # return HttpResponse(json.dumps(response), content_type="application/json")


        # try:
    #     response2['image'] = countdown.image.url
    # except ValueError:
    #     response2['image'] = None
    # response['response'] = response2
    # return HttpResponse(json.dumps(response), content_type="application/json")

    # try:
    #     title = method['title']
    # except MultiValueDictKeyError:
    #     response['status'] = 400
    #     response['error'] = 'Missing required argument: title' + '\nrequest:\n{}'.format(request)
    #     return HttpResponse(json.dumps(response), content_type='application/json')
    # try:
    #     brief_description = method['description']
    # except MultiValueDictKeyError:
    #     response['status'] = 400
    #     response['error'] = 'Missing required argument: description'
    #     return HttpResponse(json.dumps(response), content_type='application/json')
    # try:
    #     end_datetime = datetime.datetime.strptime(method['end_datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    # except MultiValueDictKeyError:
    #     response['status'] = 400
    #     response['error'] = 'Missing required argument: end_datetime'
    #     return HttpResponse(json.dumps(response), content_type='application/json')
    # # try:
    # #     image = method['image'] # TODO:
    # # except MultiValueDictKeyError:
    # #     image = None
    # try:
    #     user = User.objects.get(username=username)
    # except ObjectDoesNotExist:
    #     response['status'] = 400
    #     response['error'] = 'User does not exist: {}'.format(username)
    #     return HttpResponse(json.dumps(response), content_type='application/json')
    # countdown = Countdown()
    # countdown.user = user
    # countdown.title = title
    # countdown.brief_description = brief_description
    # countdown.end_datetime = end_datetime
    # # countdown.image = image
    # countdown.save()
    # countdown.id_string = '{}'.format(countdown.id)
    # countdown.id_string += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    # countdown.save()
    # response['status'] = 200
    # response2 = {}
    # response2['title'] = countdown.title
    # response2['description'] = countdown.brief_description
    # response2['end_datetime'] = countdown.end_datetime.isoformat() + 'Z'
    # try:
    #     response2['image'] = countdown.image.url
    # except ValueError:
    #     response2['image'] = None
    # response['response'] = response2
    # return HttpResponse(json.dumps(response), content_type="application/json")

def update_countdown(request):
    username = request.user
    response = {'status': None, 'error': None, 'response': None}
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'User does not exist: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type='application/json')
    method = request.POST
    try:
        id_string = method['id_string']
    except MultiValueDictKeyError:
        response['status'] = 400
        response['error'] = 'Missing required argument: id_string'
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        countdown = Countdown.objects.get(id_string=id_string)
    except ObjectDoesNotExist:
        response['status'] = 400
        response['error'] = 'Countdown not found: id_string: {}'.format(id_string)
        return HttpResponse(json.dumps(response), content_type='application/json')
    if countdown.user != user:
        response['status'] = 400
        response['error'] = 'Unauthorised request: username: {}'.format(username)
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        try:
            end_datetime = datetime.datetime.strptime(method['end_datetime'], '%Y-%m-%d-%H-%M-%S')
            countdown.end_datetime = end_datetime
        except MultiValueDictKeyError:
            pass
        try:
            title = method['title']
            countdown.title = title
        except MultiValueDictKeyError:
            pass
        try:
            brief_description = method['description']
            countdown.brief_description = brief_description
        except MultiValueDictKeyError:
            pass
        # try:
        #     image = method['image']
        #     countdown.image = image
        # except MultiValueDictKeyError:
        #     pass
        countdown.save()
        response['status'] = 200
        x = {} # countdown attributes to return
        x['title'] = countdown.title
        x['description'] = countdown.brief_description
        x['end_datetime'] = countdown.end_datetime.isoformat() + 'Z'
        x['id_string'] = countdown.id_string
        try:
            x['image'] = countdown.image.url
        except ValueError:
            x['image'] = None
        response['response'] = x
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
        id_string = request.POST['id_string']
        countdown = Countdown.objects.get(id_string=id_string)
    except MultiValueDictKeyError:
        response['status'] = 400
        response['error'] = 'Missing required argument: id_string'
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
