# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160522_1835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='ta_name',
            new_name='tb_name',
        ),
    ]
