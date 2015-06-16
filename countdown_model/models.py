from datetime import datetime
from django.forms import ModelForm
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Countdown(models.Model):
    title = models.CharField(max_length=200)
    brief_description = models.CharField(max_length=1000)
    entry_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True, null=True)
    end_datetime = models.DateTimeField()
    id_string = models.CharField(max_length=100)
    
class CountdownForm(ModelForm):
    class Meta:
        model = Countdown
        fields = ['title', 'brief_description', 'image', 'end_datetime']
        labels = {'brief_description': _('description')}

class ProfilePicture(models.Model):
    image = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User)
