from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [
    url(r'^info/$', views.index, name='info'),
]