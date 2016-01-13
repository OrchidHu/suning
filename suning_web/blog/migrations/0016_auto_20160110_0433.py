# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20160110_0352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spider',
            old_name='crawl_time',
            new_name='cycle',
        ),
    ]
