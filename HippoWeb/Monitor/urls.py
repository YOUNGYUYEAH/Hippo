from django.conf.urls import url
from HippoWeb.Monitor import views

urlpatterns = [
    # 接口型页面
    url(r'^i$', views.collect, name='/monitor/i'),
    url(r'^s$', views.search, name='/monitor/s'),
    url(r'^c$', views.create, name='/monitor/c'),
    # 模块展现页面
    url(r'^data', views.data, name='/monitor/data'),
    url(r'^chart$', views.chart, name='/monitor/chart'),
]
