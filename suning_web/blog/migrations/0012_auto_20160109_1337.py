# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_partner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7'),
            preserve_default=True,
        ),
    ]
