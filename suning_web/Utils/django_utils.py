#coding: utf-8
#!/usr/bin/env python
import re
from django.contrib.auth import get_user_model
import _mysql_exceptions
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.serializers import json
from django.http import HttpResponse
from suning_web import settings
import json
User = get_user_model()


class ArgsMixin(object):

    def dispatch(self, *args, **kwargs):
        request = self.request
        method = request.method
        method_args_map = {
            'GET': request.GET,
            'POST': request.POST,
            'DELETE': request.GET,
        }
        self.args = method_args_map[method]
        if settings.DEBUG:
            payload = self.request.POST.urlencode()
        injection_ret = self._dispatch_injection(*args, **kwargs)
        if injection_ret:
            return injection_ret
        try:
            return super(ArgsMixin, self).dispatch(*args, **kwargs)
        except _mysql_exceptions.Warning:
            pass
            from Utils.django_utils import JsonError
            return JsonError(u'您的输入不合法， 请正确填写后重试。')
        except ValidationError as err:
            return JsonError(str(err.message))

    def get_arg(self, arg_key):
        return self.args.get(arg_key, '').strip()

    def _dispatch_injection(self, *args, **kwargs):
        """ 执行method方法前的注入点，返回任何非空值将导致dispatch直接返回"""
        return

    def _list_ret(self, request, format_float=True):
        query_set = self._query_set()
        page = int(self.get_arg("page") or 1)
        page_size = 5
        total_count = query_set.count()
        total_page = total_count / page_size
        if (total_count % page_size):
            total_page += 1
        datas = query_set[((page - 1) * page_size):(page * page_size)]
        ret = {
            "datas": self._parse_datas(datas),
            "page": page,
            "total_page": total_page,
        }
        return ret

    def get_instance(self, _id, model):
        try:
            return model.objects.get(id=_id)
        except Exception:
            return None

    def _invalid(self):
        from Utils.django_utils import JsonError
        return JsonError(u"无效的数据", reload=1)


FRONT_TIME_STRING = "%Y-%m-%d %H:%M"


def json_default(obj):
    '''Default JSON serializer for our project.'''

    if isinstance(obj, datetime.datetime):
        return obj.strftime(FRONT_TIME_STRING)


def JsonResponse(ret, *args, **kwargs):
    kwargs["default"] = kwargs.get("default") or json_default
    return HttpResponse(json.dumps(ret, *args, **kwargs),
                        content_type='application/json; charset=utf-8')


def JsonError(msg='', dump_kwargs=None, **kwargs):
    """ msg: 反馈给用户的信息
    kwargs: 会直接作为Json数据返回
    """
    if not dump_kwargs:
        dump_kwargs = {
            "ensure_ascii": False,
        }
    ret = {
        'stat': 'error',
        'msg': msg,
    }
    ret.update(kwargs)
    return JsonResponse(ret, **dump_kwargs)


def JsonSuccess(msg='', dump_kwargs=None, **kwargs):
    """ msg: 反馈给用户的信息
    kwargs: 会直接作为Json数据返回
    """
    if not dump_kwargs:
        dump_kwargs = {
            "ensure_ascii": False,
        }
    ret = {
        'stat': 'success',
        'msg': msg,
    }
    ret.update(kwargs)
    return JsonResponse(ret, **dump_kwargs)


def normalize_phone(phone):
    return re.sub("[^0-9]", "", phone) or phone


def get_or_create_user(phone):
    phone = normalize_phone(phone)
    try:
        user = User.objects.get(username=phone)
    except Exception:
        user = User.objects.create_user(
            phone,
            password=phone,
        )
    return user


def JsonLog(msg, dump_kwargs=None, **kwargs):
    """ msg: 反馈给用户的信息
    kwargs: 会直接作为Json数据返回
    """
    if not dump_kwargs:
        dump_kwargs = {
            "ensure_ascii": False,
        }
    ret = {
        'stat': 'log',
        'msg': msg,
    }
    ret.update(kwargs)
    return JsonResponse(ret, **dump_kwargs)