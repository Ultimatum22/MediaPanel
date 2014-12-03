# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImage',
            fields=[
                ('path', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('taken_by', models.CharField(max_length=255, null=True, blank=True)),
                ('album', models.CharField(max_length=255)),
                ('date_taken', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
