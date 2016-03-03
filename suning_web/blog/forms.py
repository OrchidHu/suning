# coding: utf-8
from django.contrib.auth import authenticate, get_user_model
import re
from django import forms
from blog.models import Spider
from Utils import regex
User = get_user_model()


class RegisterForm(forms.Form):

    phone = forms.CharField(
        label=u'电话',
        error_messages={
            'required': '请输入手机号码'
        }
    )
    password = forms.CharField(
        label=u'密码',
        widget=forms.PasswordInput,
        min_length=6,
        error_messages={
            'required': '请输入密码',
            'min_length': '确保该变量至少包含 6 位字符'
        }
    )
    password2 = forms.CharField(
        label=u'确认密码',
        widget=forms.PasswordInput,
        error_messages={
            'required': '请确认密码',
        }
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not re.search(regex.RE_PHONE, phone):
            raise forms.ValidationError('请输入正确的电话号码')
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError('电话号码已存在')
        return phone

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return password2

    class Meta:
        fields = (
            'phone',
            'password'
        )
        error_messages = {
            "phone": {
                "max_length": u"输入正确的电话号码",
                "unique": u"此电话已经注册了"
            },
        }


class LoginForm(forms.Form):

    phone = forms.CharField(
        label=u'电话',
        error_messages={
            'required': '请输入手机号码'
        }
    )
    password = forms.CharField(
        label=u'密码',
        widget=forms.PasswordInput,
        error_messages={
            'required': '请输入密码',
        }
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not re.search(regex.RE_PHONE, phone):
            raise forms.ValidationError('请输入正确的电话号码')
        return phone

    def clean_password(self):
        phone = self.cleaned_data.get("phone")
        password = self.cleaned_data.get("password")
        if phone and not User.objects.filter(username=phone):
            raise forms.ValidationError('该手机号码未注册')
        if len(password) < 6:
            raise forms.ValidationError('请确保密码个数至少为六位')
        return password


class SpiderForm(forms.ModelForm):

    class Meta:
        model = Spider
        fields = (
            'cycle', 'url'
        )
        error_messages = {
            'required': u"请选择间隔抓取时间"
        }
