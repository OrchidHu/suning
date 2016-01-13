# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20160105_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=20, null=True, verbose_name='\u59d3\u540d', blank=True),
            preserve_default=True,
        ),
    ]
