# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150826_2144'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Udata',
            new_name='Updata',
        ),
    ]
