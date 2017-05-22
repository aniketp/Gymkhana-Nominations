from django.conf.urls import url, include
from django.contrib import admin
from nomi import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nominations/', include(urls))
]
