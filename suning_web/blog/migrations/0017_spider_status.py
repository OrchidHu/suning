# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20160110_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='spider',
            name='status',
            field=models.CharField(default=b'run', max_length=10, verbose_name='\u72b6\u6001'),
            preserve_default=True,
        ),
    ]
