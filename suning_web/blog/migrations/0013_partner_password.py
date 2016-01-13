# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20160109_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='password',
            field=models.CharField(max_length=20, null=True, verbose_name='\u5bc6\u7801'),
            preserve_default=True,
        ),
    ]
