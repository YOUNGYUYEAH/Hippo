from django.conf.urls import url
from HippoWeb.Monitor import views

urlpatterns = [
    url(r'i$', views.collect, name='/monitor/i'),
    url(r'^serverlist$', views.serverlist, name='/monitor/serverlist'),
    url(r'^monitordata$', views.monitordata, name='/monitor/monitordata'),
    url(r'^c$', views.monitor_cpu, name='/monitor/c'),
    url(r'^d$', views.monitor_disk, name='/monitor/d'),
    url(r'^m$', views.monitor_memory, name='/monitor/m'),
    url(r'^n$', views.monitor_network, name='/monitor/n'),
    url(r'^addserver$', views.addserver, name='/monitor/addserver'),
    url(r'^charts$', views.charts, name='/monitor/charts'),
]
