from django.conf.urls import url
from . import views

# app_name = 'nomi'

urlpatterns = [
    # nominations/
    url(r'^$', views.index, name='index'),
    url(r'^admin_portal$', views.admin_portal, name='admin_portal'),

    # nominations/clubs
    url(r'^clubs', views.club_list, name='club_list'),

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
    url(r'^applicants/(?P<pk>\d+)/$', views.applications, name='applicants'),

    # nominations/answers/2
    url(r'^answers/(?P<pk>\d+)/$', views.nomination_answer, name='nomi_answer'),

    # nominations/applicants/2 (redirect)
    url(r'^accept/(?P<pk>\d+)/$', views.accept_nomination, name='accept'),
    url(r'^reject/(?P<pk>\d+)/$', views.reject_nomination, name='reject'),
    url(r'^interviewed/(?P<pk>\d+)$', views.mark_as_interviewed, name='interviewed'),
    url(r'^append/fdybdjhhvjdk5878fkjjgj521/(?P<pk>\d+)$',views.append_user, name='append_user'),
    url(r'^append/fdybdjhhvjdk5878fkjjgj521/(?P<pk>\d+)$',views.replace_user, name='replace_user'),

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
    url(r'^createclub/(?P<pk>\d+)/$', views.club_create, name='club_create'),

    # nominations/club_approve/2/34
    url(r'^club_approve/(?P<club_pk>\d+)/(?P<view_pk>\d+)/$', views.club_approval, name='club_approval'),

    # nominations/post_approve/2/34
    url(r'^post_approve/(?P<post_pk>\d+)/(?P<view_pk>\d+)/$', views.post_approval, name='post_approval'),


    # nominations/final_post_approve/2/43
    url(r'^final_post_approve/(?P<post_pk>\d+)/(?P<view_pk>\d+)/$', views.final_post_approval,
        name='final_post_approval'),

    # nominations/child_post/2/8
    url(r'^child_post/(?P<pk>\d+)/$', views.child_post_view, name='child_post'),

    # nominations/child_post/2/8
    url(r'^child_club/(?P<pk>\d+)/(?P<view_pk>\d+)/$', views.child_club_view, name='child_club'),

    # nominations/nomi_detail/2/34/6
    url(r'^nomi_detail/(?P<nomi_pk>\d+)/$', views.nomi_detail, name='nomi_detail'),

    # nominations/post_approve/2/34
    url(r'^nomi_approve/(?P<nomi_pk>\d+)/$', views.nomi_approval, name='nomi_approval'),

    # nominations/final_nomi_approve/2/43/21
    url(r'^final_nomi_approve/(?P<nomi_pk>\d+)/$', views.final_nomi_approval, name='final_nomi_approval'),
    url(r'^group_nomi/(?P<pk>\d+)/$', views.group_nominations, name='nomi_group'),

]
