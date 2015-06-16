# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countdown_model', '0003_auto_20150616_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countdown',
            name='end_datetime',
        ),
        migrations.AddField(
            model_name='countdown',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='countdown',
            name='end_time',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
