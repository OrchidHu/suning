# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_spider_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spider',
            name='email',
            field=models.EmailField(max_length=100, null=True, verbose_name='\u90ae\u4ef6\u901a\u77e5\u5730\u5740'),
            preserve_default=True,
        ),
    ]
