from django.conf.urls import url
from HippoWeb import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^index/$', views.index, name='/index/'),
    url(r'^login/$', views.login, name='/login/'),
    url(r'^login/i$', views.checklogin, name='/login/i'),
    url(r'^logout/$', views.logout, name='/logout/'),
]

handler404 = views.page_not_found
handler500 = views.server_error
