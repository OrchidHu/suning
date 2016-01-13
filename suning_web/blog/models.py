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

    ident = models.CharField(
        verbose_name=u"商品编号",
        max_length=20
    )
    title = models.CharField(
        verbose_name=u"品牌",
        max_length=20
    )
    name = models.CharField(
        verbose_name=u"商品名",
        max_length=200
    )
    comment = models.CharField(
        verbose_name=u"评论条数",
        max_length=20
    )
    link = models.CharField(
        verbose_name=u"商品链接",
        max_length=100
    )
    price = models.CharField(
        verbose_name=u"当前价",
        max_length=20
    )
    crawl_time = models.CharField(
        verbose_name=u"抓取时间",
        max_length=20
    )

    def __unicode__(self):
        return self.name, self.link, self.comment, self.price


class Partner(models.Model):

    user = models.OneToOneField(
        User,
        related_name='partner_user',
        verbose_name=u'客户',
    )
    name = models.CharField(
        verbose_name=u'姓名',
        max_length=20,
        null=True,
        blank=True
    )
    phone = models.CharField(
        verbose_name=u"手机号",
        max_length=20
    )
    password = models.CharField(
        verbose_name=u"密码",
        max_length=20,
        null=True
    )

    def __unicode__(self):
        return self.name, self.phone


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

    cycle = models.CharField(
        verbose_name=u'抓取间隔时间',
        max_length=50,
        choices=TIME,
        default=3600*24
    )


admin.site.register(Partner)
