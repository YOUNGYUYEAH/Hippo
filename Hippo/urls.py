from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
admin.autodiscover()

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include('HippoWeb.urls')),
    url(r'^monitor/', include('HippoWeb.Monitor.urls')),
    url(r'^static/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_ROOT})
]
