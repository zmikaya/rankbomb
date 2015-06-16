# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicedata',
            name='ip',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]
