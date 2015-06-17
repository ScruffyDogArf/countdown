# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countdown_model', '0004_auto_20150616_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='countdown',
            name='archived',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='countdown',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images', blank=True),
        ),
    ]
