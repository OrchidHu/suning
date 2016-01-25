# coding:utf-8

import datetime
import time
from django.shortcuts import render_to_response, resolve_url, redirect
from django.views.generic import TemplateView
import subprocess
from blog.models import (
    Updata,
    Shopping,
    Partner
)
from Utils.django_utils import (
    get_or_create_user,
    ArgsMixin,
    JsonError,
    JsonSuccess,
)
from django.core.paginator import Paginator
from . import forms


class Index(ArgsMixin, TemplateView):
    def get(self, request):
        self.page = self.get_arg("page")
        if not self.page:
            self.page = '1'
        page = int(self.page) - 1
        if page < 0:
            page = 0
            self.page = '1'
        records = Updata.objects.values()
        self.context = []
        all_shopping = Shopping.objects.values()
        if len(records) != 0:
            last_time = time.localtime(float(records[len(records) - 1]['crawl_time']))
            last_day = last_time.tm_mday
            for record in records:
                crawl_time = time.localtime(float(record['crawl_time'])).tm_mday
                # 展示最后一次抓取当天价格有变化的数据
                if crawl_time != last_day:
                    continue
                for shopping in all_shopping:
                    if shopping['ident'] == record['ident']:
                        dict_key = ['ident', 'name', 'link', 'price', 'last_price', 'crawl_time']
                        tm = str(last_time.tm_year) + "-" + str(last_time.tm_mon) + "-" + str(last_day)
                        dict_value = [shopping['ident'], shopping['name'], shopping['link'], record['price'],
                                      record['last_price'], tm]
                        lists = dict(zip(dict_key, dict_value))
                        self.context.append(lists)
        p = Paginator(self.context, 20)
        page_list = p.page_range
        if page >= len(page_list):
            self.page = len(page_list)
            page = self.page
        if len(page_list) <= 5:
            pass
        elif page <= 2:
            page_list = page_list[0:5]
        elif page >= len(page_list) - 2:
            page_list = page_list[len(page_list) - 5:len(page_list)]
        else:
            page_list = [x for x in page_list[page - 2:page + 3] if x > 0]
        return render_to_response(
            'blog/base.html',
            {
                'context': p.page(self.page),
                'page_list': page_list,
                'num_pages': p.num_pages,
                'page': self.page
            }
        )


class Tool(ArgsMixin, TemplateView):
    def get(self, request):
        ident = self.get_arg("phone_id")
        records = Updata.objects.values()
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
            user = get_or_create_user(username)
            user.set_password(password)
            partner, created = Partner.objects.get_or_create(
                phone=username,
                defaults={
                    "user": user,
                    "name": username,
                }
            )
            partner.password = form.cleaned_data.get("password")
            partner.save()
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
            request.session['username'] = form.cleaned_data.get('phone')
            return redirect("blog:spider")
        context["form"] = form
        return self.render_to_response(context)


class Spider(ArgsMixin, TemplateView):
    template_name = "blog/spider.html"

    def __init__(self):
        self.proc = None

    def get(self, request):
        context = self.get_context_data()
        username = request.session.get('username')
        kill = request.GET.get("kill")
        pid = request.GET.get("pid")
        if pid:
            pass
        if kill:
            self.proc = request.GET.get("proc")
            subprocess.Popen('kill -9 %s' % self.proc, shell=True)
            context["p"] = 0
        if username:
            form = forms.SpiderForm()
            context['form'] = form
            return self.render_to_response(context)
        return redirect("blog:login")

    def post(self, request):
        context = self.get_context_data()
        form = forms.SpiderForm()
        cycle = request.POST.get("cycle")
        self.proc = subprocess.Popen('python /home/huwei/hello.py %s' % cycle, stdout=subprocess.PIPE, shell=True)
        context["form"] = form
        context["p"] = 1
        context["proc"] = self.proc.pid
        return self.render_to_response(context)
