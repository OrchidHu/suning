from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from . import views

urlpatterns=[
    url(
        r'^$',
        views.Index.as_view(),
        name='index'
    ),
    url(
        r'^tool/$',
        views.Tool.as_view(),
        name='tool'
    ),
    url(
        r'^register/$',
        views.Register.as_view(),
        name='register'
    ),
    url(
        r'^login/$',
        views.Login.as_view(),
        name='login'
    ),
    url(
        r'^spider/$',
        login_required(views.Spider.as_view()),
        name='spider'
    )
]
