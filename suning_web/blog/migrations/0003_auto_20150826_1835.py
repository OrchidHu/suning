# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150826_1834'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Phones',
            new_name='Shopping',
        ),
    ]
