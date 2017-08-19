from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [

    url(r'^$', views.post_holder_search, name='info'),
    url(r'^mail_id/(?P<query>.+)/$', views.get_mail, name='get_id'),


]