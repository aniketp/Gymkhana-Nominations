from django.conf.urls import url
from . import views

urlpatterns = [
    # nominations/
    url(r'^$', views.index, name='index'),

    # nominations/2
    url(r'^(?P<pk>\d+)/$', views.nomi_apply, name='nomi_apply'),

    # nominations/result/2
    url(r'^result/(?P<pk>\d+)/$', views.result, name='result')

]