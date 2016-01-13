# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150826_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopping',
            name='link',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
