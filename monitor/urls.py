from django.conf.urls import url
from monitor import views

urlpatterns = [
    url(r'i$', views.minitorjson, name="/monitor/i"),
]
