from django.conf.urls import url
from HippoWeb.Monitor import views as mv

urlpatterns = [
    url(r'i$', mv.collect, name='/monitor/i'),
    url(r'^serverlist$', mv.serverlist, name='/monitor/serverlist'),
    url(r'^monitordata$', mv.monitordata, name='/monitor/monitordata'),
]
