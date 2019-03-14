from django.contrib import admin
from django.urls import path
from django.conf.urls import re_path, url, include
from django.contrib import admin
admin.autodiscover()
from HippoWeb import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.login),
]
