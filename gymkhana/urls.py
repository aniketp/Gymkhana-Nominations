from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.urls import views


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^nominations/', include('nomi.urls')),
    url(r'^$', RedirectView.as_view(url='/nominations/')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
