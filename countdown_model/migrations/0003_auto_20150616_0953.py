# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countdown_model', '0002_auto_20150616_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countdown',
            name='image',
            field=models.ImageField(null=True, upload_to=b'/Users/admin/projects/countdown/countdownenv/countdown/media', blank=True),
        ),
    ]
