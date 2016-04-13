# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.CharField(max_length=15, unique=True, null=True, verbose_name='\u8bc4\u8bba')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shopping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.CharField(max_length=20, verbose_name='\u5546\u54c1\u7f16\u53f7')),
                ('name', models.CharField(max_length=200, verbose_name='\u5546\u54c1\u540d')),
                ('price', models.CharField(max_length=20, verbose_name='\u5f53\u524d\u4ef7')),
                ('crawl_time', models.CharField(max_length=20, verbose_name='\u6293\u53d6\u65f6\u95f4')),
                ('ch_price', models.CharField(max_length=10, verbose_name='\u4ef7\u683c\u53d8\u5316')),
                ('image_url', models.CharField(max_length=500, verbose_name='\u56fe\u7247')),
                ('url', models.CharField(max_length=500, verbose_name='\u5546\u54c1\u7f51\u5740')),
                ('user', models.ForeignKey(related_name='shopping_user', verbose_name='\u8d27\u4e3b', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(max_length=5000, null=True)),
                ('cycle', models.CharField(default=86400, max_length=20, verbose_name='\u6293\u53d6\u95f4\u9694\u65f6\u95f4', choices=[(1800, '\u534a\u5c0f\u65f6'), (3600, '\u4e00\u5c0f\u65f6'), (7200, '\u4e24\u5c0f\u65f6'), (18000, '\u4e94\u5c0f\u65f6'), (86400, '\u4e00\u5929'), (172800, '\u4e24\u5929'), (518400, '\u4e00\u5468')])),
                ('start_time', models.CharField(max_length=50, null=True, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('email', models.EmailField(max_length=100, null=True, verbose_name='\u90ae\u4ef6\u901a\u77e5\u5730\u5740:')),
                ('user', models.ForeignKey(related_name='pa_spider', verbose_name=b'\xe4\xb8\xaa\xe4\xba\xba\xe7\x88\xac\xe8\x99\xab', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
