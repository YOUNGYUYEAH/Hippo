from django.conf.urls import url
from HippoWeb.Monitor import views

urlpatterns = [
    url(r'^i$', views.collect, name='/monitor/i'),
    url(r'^s$', views.search, name='/monitor/s'),
    url(r'^data', views.data, name='/monitor/data'),  # 实际生产中这个页面要屏蔽
    url(r'^chart$', views.chart, name='/monitor/chart'),
    url(r'^addserver$', views.addserver, name='/monitor/addserver'),
]
