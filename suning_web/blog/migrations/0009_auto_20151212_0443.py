# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_auto_20151210_0533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name='\u59d3\u540d')),
                ('phone', models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7')),
                ('user', models.OneToOneField(related_name='partner_user', verbose_name='\u5ba2\u6237', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='shopping',
            name='comment',
            field=models.CharField(max_length=20, verbose_name='\u8bc4\u8bba\u6761\u6570'),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='crawl_time',
            field=models.CharField(max_length=20, verbose_name='\u6293\u53d6\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='ident',
            field=models.CharField(max_length=20, verbose_name='\u5546\u54c1\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='link',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u94fe\u63a5'),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='name',
            field=models.CharField(max_length=200, verbose_name='\u5546\u54c1\u540d'),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='price',
            field=models.CharField(max_length=20, verbose_name='\u5f53\u524d\u4ef7'),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='title',
            field=models.CharField(max_length=20, verbose_name='\u54c1\u724c'),
        ),
        migrations.AlterField(
            model_name='updata',
            name='crawl_time',
            field=models.CharField(max_length=50, verbose_name='\u6293\u53d6\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='updata',
            name='ident',
            field=models.CharField(max_length=20, verbose_name='\u5546\u54c1\u7f16\u53f7'),
        ),
        migrations.AlterField(
            model_name='updata',
            name='last_price',
            field=models.CharField(max_length=20, verbose_name='\u539f\u4ef7'),
        ),
        migrations.AlterField(
            model_name='updata',
            name='price',
            field=models.CharField(max_length=20, verbose_name='\u5f53\u524d\u4ef7'),
        ),
    ]
