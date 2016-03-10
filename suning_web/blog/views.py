# coding:utf-8
import MySQLdb

import datetime, time
from django.contrib.auth import authenticate, get_user_model, login, logout
import time, models
from django.shortcuts import render_to_response, redirect
from django.views.generic import TemplateView

from blog.models import (
    Shopping,
)
from Utils.django_utils import (
    ArgsMixin,
)
from . import forms
User = get_user_model()


class Index(ArgsMixin, TemplateView):
    template_name = 'blog/base.html'

    def get(self, request):
        if not request.user.id:
            return redirect("blog:login")
        context = self.get_context_data()
        idents = []
        context['shopping'] = []
        all_shopping = Shopping.objects.filter(user_id=request.user.id)
        if not all_shopping.first():
            spider = models.Spider.objects.filter(user_id=request.user.id)
            if spider:
                context['error_url'] = 'error_url'
        for shopping in all_shopping.reverse()[::-1]:
            if shopping.ident not in idents:
                idents.append(shopping.ident)
                context['shopping'].append(shopping)
        context['username'] = request.user.username
        return self.render_to_response(context)


class Tool(ArgsMixin, TemplateView):
    def get(self, request):
        ident = self.get_arg("phone_id")
        records = Shopping.objects.values()
        now_time = datetime.datetime.now()
        for record in records:
            if record['ident'] == ident:
                earliest_time = time.localtime(float(record['crawl_time']))
                break
        # 计算最早记录到现在的时间相隔天数 记为days
        old_day = datetime.datetime(earliest_time.tm_year, earliest_time.tm_mon, earliest_time.tm_mday)
        today = datetime.datetime(now_time.year, now_time.month, now_time.day)
        days = (today - old_day).days + 1
        if days >= 0:
            context = []
            # 时间又最早推算到现在,方便价格走势计算
            lowest_price = records[0]['price']
            for i in range(days)[::-1]:
                # 计算当期时间之前的每一天
                tm = now_time - datetime.timedelta(days=i)
                search = 'no'
                em = []
                for i in range(len(records))[::-1]:  # 倒序,方便找到一天中最后一次变化的价格
                    # 找到对应编号的记录
                    if records[i]['ident'] == ident:
                        crawl_time = time.localtime(float(records[i]['crawl_time']))
                        # 判断此记录时间与i天前的时间是否一样
                        if crawl_time.tm_year == tm.year and crawl_time.tm_mon == tm.month and crawl_time.tm_mday == tm.day:
                            em.append(tm.year)
                            em.append(tm.month)
                            em.append(tm.day)
                            # 价格有变,把价格调为记录中的价格
                            price = int(eval(records[i]['price'].encode('utf-8')))
                            if price < lowest_price:
                                lowest_price = price
                            em.append(price)
                            context.append(em)
                            search = 'ok'
                            # 如果当日有多次变动,则获取最后一次变动的价格
                            break
                if search == 'no':
                    em.append(tm.year)
                    em.append(tm.month)
                    em.append(tm.day)
                    # 此次价格和上次价格一样,没有变化
                    em.append(price)
                    context.append(em)
        context.reverse()
        word = '单一价格'
        if len(context) >= 2:
            if context[0][3] > context[1][3]:
                word = '价格上涨'
            elif context[0][3] < context[1][3]:
                word = '价格下降'
            else:
                word = '价格平稳'
        return render_to_response('blog/tool.html', {'context': context, 'lowest': lowest_price, 'word': word})


class Register(ArgsMixin, TemplateView):
    template_name = "blog/register.html"

    def get(self, request):
        context = self.get_context_data()
        form = forms.RegisterForm()
        context["form"] = form
        return self.render_to_response(context)

    def post(self, request):
        context = self.get_context_data()
        form = forms.RegisterForm(request.POST)
        context["form"] = form
        if form.is_valid():
            username = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(
                username,
                password=password,
            )
            user.is_active = True
            user.is_staff = True
            user.set_password(password)
            user.save
            return redirect("blog:login")
        context["errors"] = form.errors
        return self.render_to_response(context)


class Login(ArgsMixin, TemplateView):
    template_name = "blog/login.html"

    def get(self, request):
        context = self.get_context_data()
        form = forms.LoginForm()
        context["form"] = form
        return self.render_to_response(context)

    def post(self, request):
        context = self.get_context_data()
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            user = authenticate(username=phone, password=password)
            if not user:
                context["errors"] = u"账户密码错误"
            else:
                login(request, user)
                return redirect("blog:index")
        context["form"] = form
        return self.render_to_response(context)


class Logout(ArgsMixin, TemplateView):

    def get(self, request):
        logout(request)
        return redirect("blog:login")


class Spider(ArgsMixin, TemplateView):
    template_name = "blog/spider.html"

    def __init__(self):
        self.proc = None
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='suning', port=3306, charset='utf8')
        self.cursor = self.conn.cursor()

    def get(self, request):
        context = self.get_context_data()
        kill_spider = request.GET.get("kill")
        if kill_spider:
            self.cursor.execute('DELETE FROM blog_shopping WHERE user_id=%s' % request.user.id)
            self.cursor.execute('DELETE FROM blog_spider WHERE user_id=%s' % request.user.id)
            self.conn.commit()
        if request.user.is_authenticated():
            form = forms.SpiderForm()
            spider = self.cursor.execute('SELECT id FROM suning.blog_spider WHERE user_id=%s' % request.user.id)
            if spider:
                context["spider"] = u"关闭"
            context['form'] = form
            context['username'] = request.user.username
            return self.render_to_response(context)
        return redirect("blog:login")

    def post(self, request):
        self.context = self.get_context_data()
        form = forms.SpiderForm()
        cycle = self.get_arg("cycle")
        urls = self.get_urls()
        email = self.get_email()
        self.context["form"] = form
        if not self.context['msg'] and not self.context['email_er']:
            spider = models.Spider.objects.create(user_id=request.user.id)
            spider.url = urls
            spider.email = email
            spider.cycle = cycle
            spider.start_time = time.time()+1
            spider.save()
        excise_spider = self.cursor.execute('SELECT * FROM blog_spider WHERE user_id=%s' % request.user.id)
        if excise_spider:
            self.context["spider"] = u"关闭"
        self.context['username'] = request.user.username
        return self.render_to_response(self.context)

    def get_email(self):
        self.context['email_er'] = {}
        email_select = self.get_arg("email-select")
        email = self.get_arg("email")
        if email_select == "yes":
            self.context['selected'] = 'yes'
            if not email:
                self.context['email_er'] = u"请填写邮箱地址"
        return email

    def get_urls(self):
        urls = self.get_arg("url").replace('\r\n', ',')
        self.context['msg'] = {}
        if not urls:
            self.context['msg'] = u"请填写网址"
        if len(urls.split(',')) > 10:
            self.context['msg'] = u"已超过十个商品"
        return urls

