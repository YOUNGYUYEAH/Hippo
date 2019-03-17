from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from HippoWeb.views import page_not_found, page_error

admin.autodiscover()
handler404 = page_not_found
handler500 = page_error
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('HippoWeb.urls')),
    url(r'^static/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_ROOT})
]
