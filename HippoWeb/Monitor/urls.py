from django.conf.urls import url
from HippoWeb.Monitor import views

urlpatterns = [
    url(r'i$', views.collect, name='/monitor/i'),
    url(r'alerm', views.monitor_alerm, name='/monitor/alerm'),
    url(r'info$', views.monitor_info, name='/monitor/info')
]
