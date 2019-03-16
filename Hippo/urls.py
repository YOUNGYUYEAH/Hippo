from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()
from HippoWeb import views


urlpatterns = [
    url(r'^$', views.login),
    url(r'^index/$', views.index, name="/index/"),
    url(r'^login/$', views.login, name="/login/"),
    url(r'^login/i$', views.checklogin, name="/login/i"),
    url(r'^logout/$', views.logout, name="/logout/")
]
