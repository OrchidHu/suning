# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('comment', models.CharField(max_length=20)),
                ('link', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=20)),
                ('crawl_time', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Shopping',
        ),
    ]
