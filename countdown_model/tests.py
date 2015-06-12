import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from countdown.models import Countdown

# Create your tests here.
class MainTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="dkv")
        countdown = Countdown.objects.create(title="title",
                                             brief_description="description",
                                             user=user,
                                             image="",
                                             end_datetime=datetime.datetime.now() + datetime.timedelta(days=1),
                                             id_string="test0")

    def test_animals_can_speak(self):
         """Animals that can speak are correctly identified"""
         countdown = Countdown.objects.get(pk=1)
         client = Client()
         response = client.get("/api")
         print response
