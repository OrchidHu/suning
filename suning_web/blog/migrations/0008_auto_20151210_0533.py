# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20150930_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updata',
            name='crawl_time',
            field=models.CharField(max_length=50),
        ),
    ]
