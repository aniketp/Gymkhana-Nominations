from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nominations/', include('nomi.urls')),
    url(r'^forms/', include('forms.urls')),
    url(r'^info/', include('info.urls')),
    url(r'^$', RedirectView.as_view(url='nominations')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
