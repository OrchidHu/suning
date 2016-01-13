# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shopping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('comment', models.CharField(max_length=20)),
                ('link', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Updata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=20)),
                ('crawl_time', models.CharField(max_length=20)),
            ],
        ),
    ]
