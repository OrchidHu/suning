# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150826_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopping',
            name='crawl_time',
            field=models.CharField(max_length=50),
        ),
    ]
