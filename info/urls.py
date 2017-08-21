from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [

    url(r'^$', views.post_holder_search, name='info'),
    url(r'^csv/(?P<session_pk>\w+)/(?P<club_pk>\w+)/(?P<post_pk>\w+)/$', views.get_csv, name='get_csv'),

]