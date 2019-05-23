from django.conf.urls import url
from HippoWeb.Monitor import views

urlpatterns = [
    url(r'^i$', views.collect, name='/monitor/i'),
    url(r'^s$', views.search, name='/monitor/s'),
    url(r'^data$', views.monitordata, name='/monitor/data'),
    url(r'^chart$', views.charts, name='/monitor/chart'),
    url(r'^addserver$', views.addserver, name='/monitor/addserver'),
    url(r'^main', views.main, name='/monitor/main')
]
