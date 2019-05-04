from django.conf.urls import url
from HippoWeb.Monitor import views

urlpatterns = [
    url(r'i$', views.collect, name='/monitor/i'),
    url(r'^serverlist$', views.serverlist, name='/monitor/serverlist'),
    url(r'^monitordata$', views.monitordata, name='/monitor/monitordata'),
    url(r'^cpu$', views.monitor_cpu, name='/monitor/cpu'),
    url(r'^disk$', views.monitor_disk, name='/monitor/disk'),
    url(r'^memory$', views.monitor_memory, name='/monitor/memory'),
    url(r'^network$', views.monitor_network, name='/monitor/network'),
    url(r'^addserver$', views.addserver, name='/monitor/addserver'),
    url(r'^charts$', views.charts, name='/monitor/charts'),
]
