# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_partner_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crawl_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6293\u53d6\u95f4\u9694\u65f6\u95f4', choices=[(1800, '\u534a\u5c0f\u65f6'), (3600, '\u4e00\u5c0f\u65f6'), (7200, '\u4e24\u5c0f\u65f6'), (18000, '\u4e94\u5c0f\u65f6'), (86400, '\u4e00\u5929'), (172800, '\u4e24\u5929'), (518400, '\u4e00\u5468')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
