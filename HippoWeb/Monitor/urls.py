from django.conf.urls import url
from HippoWeb.Monitor import views

urlpatterns = [
    url(r'i$', views.collect, name='/monitor/i'),
    url(r'^serverlist$', views.serverlist, name='/monitor/serverlist'),
    url(r'^monitordata$', views.monitordata, name='/monitor/monitordata'),
]
