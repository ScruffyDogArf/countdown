from functools import wraps
import datetime
import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from countdown_model.models import Countdown, CountdownForm

print 'countdown_model/test.py'

# Create your tests here.
class MainTestCase(TestCase):
    def setUp(self):
        print 'MainTestCase.setUp'
        # wrap the client post method
        def post_wrapper(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    api = kwargs['api']
                except KeyError:
                    api = False
                response = func(*args, **kwargs)
                if api:
                    self.assertEqual(response['Content-Type'], 'application/json', response)
                    self.assertIn('status', response.content)
                    try:
                        int(json.loads(response.content)['status'])
                    except Exception as e:
                        msg = 'response.content: {}'.format(response.content)
                        mst += '\nstatus: {}'.format(json.loads(response.content)['status'])
                        msg += '\n{}'.format(e)
                        raise Exception(msg)
                    self.assertIn('response', response.content)
                    self.assertIn('error', response.content)
                return response
            return wrapper
        self.client.post = post_wrapper(self.client.post)
        # create and login user
        user = User.objects.create_user(username="dkv", password="secret")
        response = self.client.post('/login', {'username': 'dkv', 'password': 'secret'})
        self.assertIn('_auth_user_id', self.client.session)
    def test_api(self):
        print 'MainTestCase.test_main'
        # add some data in
        post_args = {'title': 'title',
                          'brief_description':'brief description',
                          'end_date': '2015-12-25',
                          'end_time': '00:00:00'}
        response = self.client.post('/api/countdowns/create', post_args, api=True)
        # add a event that occurred in the past
        args = {
            'title': 'past event',
            'brief_description': 'past event',
            'end_date': '2013-12-25',
            'end_time': '00:00:00'
        }
        response = self.client.post('/api/countdowns/create', args, api=True)
        # an event with an image
        # response = self.client.post('/api/countdowns/create', {'title': 'event with image', 'brief_description': 'brief description', 'end_date': '2015-12-25', 'end_time': '00:00:00'})
        # update the last entry
        print response
        x = json.loads(response.content)
        id_string = json.loads(response.content)['response']['id_string']
        countdown = Countdown.objects.get(id_string=id_string)
        countdown_dict = json.loads(countdown.json())
        args = {
        }
        for field in CountdownForm.Meta.fields:
            if field != 'image':
                args[field] = countdown_dict[field]
        args['brief_description'] = 'Updated brief description'
        response = self.client.post('/api/countdowns/update/{}'.format(id_string), args, api=True)
        print response
        # countdown = Countdown.objects.get(id_string=id_string)
        # print countdown.brief_description
        # form = CountdownForm(, instance=countdown)
        # print form
        # print form.is_valid()
        # print form.errors
        # form.brief_description = 'Updated brief description'
        # form.save()
        # print countdown.brief_description
                                    

