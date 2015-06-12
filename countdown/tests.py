import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from countdown.models import Countdown

print 'django_project test'

# Create your tests here.
class MainTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dvoong", password='pbjelly')
    def test_correct_user_login(self):
        response = self.client.post('/login', {'username': 'dvoong', 'password': 'pbjelly'})
        self.assertRedirects(response, '/home', status_code=302)
        self.assertIn('_auth_user_id', self.client.session)
    def test_incorrect_user_login(self):
        response = self.client.post('/login', {'username': 'dvoong', 'password': 'pbjell'})
        self.assertRedirects(response, '/home', status_code=302)
        self.assertNotIn('_auth_user_id', self.client.session)
    def test_countdown_creation(self):
        pass
