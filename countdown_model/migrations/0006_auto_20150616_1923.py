# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countdown_model', '0005_auto_20150616_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countdown',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
