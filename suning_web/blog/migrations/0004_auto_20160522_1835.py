# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160310_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ta_name',
            field=models.CharField(default=123, max_length=15, verbose_name='\u8bc4\u8bba\u8868\u540d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spider',
            name='email',
            field=models.EmailField(max_length=100, null=True, verbose_name='\u90ae\u4ef6\u901a\u77e5\u5730\u5740:'),
            preserve_default=True,
        ),
    ]
