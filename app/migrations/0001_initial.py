# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='choiceData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=128)),
                ('compType', models.CharField(max_length=128)),
                ('matchupNames', models.CharField(max_length=5000)),
                ('choices', models.CharField(max_length=5000)),
                ('TTChoose', models.CharField(max_length=5000)),
                ('CTime', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'Choice Data',
            },
            bases=(models.Model,),
        ),
    ]
