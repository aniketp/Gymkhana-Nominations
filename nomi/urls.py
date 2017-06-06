from django.conf.urls import url
from . import views

# app_name = 'nomi'

urlpatterns = [
    # nominations/
    url(r'^$', views.index, name='index'),

    # nominations/2
    url(r'^apply/(?P<pk>\d+)/$', views.nomi_apply, name='nomi_apply'),

    # nominations/profile/
    url(r'^profile/$', views.profile_view, name='profile'),

    # nominations/profile/create
    url(r'profile/create/$', views.UserProfileCreate.as_view(), name='profile_create'),

    # nominations/profile/update/2
    url(r'^profile/update/(?P<pk>\d+)/$', views.UserProfileUpdate.as_view(), name='profile_update'),

    # nominations/result/2
    url(r'^result/(?P<pk>\d+)/$', views.result, name='result'),

    # nominations/applicants/2
    url(r'^applicants/(?P<pk>\d+)/$', views.application_result, name='applicants'),

    url(r'^answers/(?P<pk>\d+)/$', views.nomination_answer, name='nomi_answer'),

    # nominations/applicants/2 (redirect)
    url(r'^accept/(?P<pk>\d+)/$', views.accept_nomination, name='accept'),
    url(r'^reject/(?P<pk>\d+)/$', views.reject_nomination, name='reject'),

    # nominations/create
    url(r'^create/(?P<pk>\d+)/$', views.nomination_create, name='nomi_create'),

    # nominations/2/update
    url(r'^(?P<pk>\d+)/update/$', views.NominationUpdate.as_view(), name='nomi_update'),

    # nominations/2/delete
    url(r'^(?P<pk>\d+)/delete/$', views.NominationDelete.as_view(), name='nomi_delete'),

    # nominations/post/2
    url(r'^post/(?P<pk>\d+)/$', views.post_view, name='post_view'),

    # nominations/createpost/2
    url(r'^createpost/(?P<pk>\d+)/$', views.post_create, name='post_create'),

    # nominations/club/2
    url(r'^club/(?P<pk>\d+)/$', views.club_view, name='club_view'),

    # nominations/createclub/2
    # url(r'^createpost/(?P<pk>\d+)/$', views.club_create, name='club_create'),

    # nominations/filter
    url(r'^filter/$', views.universal_filter, name='universal_filter'),

    # nominations/post_approve/2/34
    url(r'^post_approve/(?P<post_pk>\d+)/(?P<view_pk>\d+)/$',views.post_approval,name='post_approval'),


    url(r'^final_post_approve/(?P<post_pk>\d+)/(?P<view_pk>\d+)/$',views.final_post_approval,name='final_post_approval'),

    # nominations/child_post/2/8
    url(r'^child_post/(?P<pk>\d+)/(?P<view_pk>\d+)/$',views.child_post_view,name='child_post'),
]
