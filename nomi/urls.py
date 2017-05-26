from django.conf.urls import url
from . import views

# app_name = 'nomi'

urlpatterns = [
    # nominations/
    url(r'^$', views.index, name='index'),

    # nominations/2
    url(r'^(?P<pk>\d+)/$', views.nomi_apply, name='nomi_apply'),

    # nominations/profile
    # url(r'^profile/$', views.)

    # nominations/result/2
    url(r'^result/(?P<pk>\d+)/$', views.result, name='result'),

    # nominations/applicants/2
    url(r'^applicants/(?P<pk>\d+)/$', views.application_result, name='applicants'),

    # nominations/applicants/2 (redirect)
    url(r'^accept/(?P<pk>\d+)/$', views.accept_nomination, name='accept'),
    url(r'^reject/(?P<pk>\d+)/$', views.reject_nomination, name='reject'),

    # nominations/create
    url(r'^create/$', views.NominationCreate.as_view(), name='nomi_create'),

    # nominations/2/update
    url(r'^(?P<pk>\d+)/update/$', views.NominationUpdate.as_view(), name='nomi_update'),

    # nominations/2/delete
    url(r'^(?P<pk>\d+)/delete/$', views.NominationDelete.as_view(), name='nomi_delete'),


]