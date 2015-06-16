# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_choicedata_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicedata',
            name='ip',
            field=models.CharField(default=0, max_length=128),
            preserve_default=True,
        ),
    ]
