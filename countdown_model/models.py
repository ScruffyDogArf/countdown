import copy, json
from datetime import datetime, timedelta
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
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    id_string = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    output_fields = ['title', 'brief_description', 'image', 'end_date', 'end_time', 'id_string']
    output_fields_current_state = ['days', 'hours', 'minutes', 'seconds', 'complete']
    input_fields = copy.deepcopy(output_fields)
    input_fields.remove('id_string')
    def json(self):
        x = {}
        self.update_state()
        for output_field in self.output_fields + self.output_fields_current_state:
            if output_field in ['end_date', 'end_time']:
                x[output_field] = str(getattr(self, output_field))
            elif output_field in ['image'] and getattr(self, output_field) == None:
                x[output_field] = ''
            elif output_field in ['image']:
                x[output_field] = getattr(self, output_field).url
            else:
                x[output_field] = getattr(self, output_field)
        return json.dumps(x)
    def update_state(self):
        end_datetime = datetime.combine(self.end_date, self.end_time)
        self.time_remaining = end_datetime - datetime.now()
        if self.time_remaining.days < 0:
            self.time_remaining = timedelta(0)
            self.complete = True
        else:
            self.complete = False
        hours, remainder = divmod(self.time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.days = self.time_remaining.days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        return self
    
class CountdownForm(ModelForm):
    class Meta:
        model = Countdown
        fields = Countdown.input_fields
        
class ProfilePicture(models.Model):
    image = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User)
