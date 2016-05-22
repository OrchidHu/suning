# coding:utf8
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Updata(models.Model):

    ident = models.CharField(
        verbose_name=u"商品编号",
        max_length=20
    )
    price = models.CharField(
        verbose_name=u"当前价",
        max_length=20
    )
    last_price = models.CharField(
        verbose_name=u"原价",
        max_length=20)
    crawl_time = models.CharField(
        verbose_name=u"抓取时间",
        max_length=50
    )

    def __unicode__(self):
        return self.price, self.ident, self.crawl_time


class Shopping(models.Model):

    user = models.ForeignKey(
        User,
        related_name='shopping_user',
        verbose_name=u'货主',
    )
    ident = models.CharField(
        verbose_name=u"商品编号",
        max_length=20
    )
    name = models.CharField(
        verbose_name=u"商品名",
        max_length=200
    )
    price = models.CharField(
        verbose_name=u"当前价",
        max_length=20
    )
    crawl_time = models.CharField(
        verbose_name=u"抓取时间",
        max_length=20
    )
    ch_price = models.CharField(
        verbose_name=u"价格变化",
        max_length=10,
    )
    image_url = models.CharField(
        verbose_name=u"图片",
        max_length=500
    )
    url = models.CharField(
        verbose_name=u"商品网址",
        max_length=500
    )

    def __unicode__(self):
        return self.name


class Comment(models.Model):

    ident = models.CharField(
        verbose_name=u"评论",
        max_length=15,
        unique=True,
        null=True
    )
    tb_name = models.CharField(
	verbose_name=u"评论表名",
	max_length=15,
    )

class Spider(models.Model):

    TIME = (
        (60*30, u"半小时"),
        (60*60, u"一小时"),
        (60*120, u"两小时"),
        (60*300, u"五小时"),
        (3600*24, u"一天"),
        (3600*48, u"两天"),
        (3600*144, u"一周")
    )
    user = models.ForeignKey(
        User,
        related_name="pa_spider",
        verbose_name="个人爬虫",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    url = models.TextField(
        max_length=5000,
        null=True
    )
    cycle = models.CharField(
        verbose_name=u'抓取间隔时间',
        max_length=50,
        choices=TIME,
        default=3600*24
    )
    start_time = models.CharField(
        verbose_name=u'开始时间',
        max_length=20,
        null=True
    )
    email = models.EmailField(
        verbose_name=u'邮件通知地址:',
        max_length=100,
        null=True,
    )

