from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nominations/', include('nomi.urls')),
    url(r'^forms/', include('forms.urls')),
    url(r'^info/', include('info.urls')),
    url(r'^$', RedirectView.as_view(url='nominations')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)