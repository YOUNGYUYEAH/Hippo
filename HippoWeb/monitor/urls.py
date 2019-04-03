from django.conf.urls import url
from HippoWeb.monitor import views

urlpatterns = [
    url(r'i$', views.minitorjson, name='/monitor/i'),
    url(r'showinfo$', views.showinfo, name='/monitor/showinfo')
]
