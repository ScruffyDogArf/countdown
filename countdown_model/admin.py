from django.contrib import admin

# Register your models here.

from .models import Countdown

admin.site.register(Countdown)
