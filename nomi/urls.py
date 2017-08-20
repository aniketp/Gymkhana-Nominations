from django.conf.urls import url
from . import views

# app_name = 'nomi'

urlpatterns = [
    # nominations/
    url(r'^$', views.index, name='index'),

    # nominations/senate
    url(r'^senate/$', views.senate_view, name='senate_view'),

    # nominations/admin_portal
    url(r'^admin_portal/$', views.admin_portal, name='admin_portal'),

    # nominations/interviews
    url(r'^interviews/$', views.interview_list, name='interviews'),

    # nominations/all
    url(r'^all/$', views.all_nominations, name='all_nominations'),
    
    # nominations/apply/2
    url(r'^apply/(?P<pk>\d+)/$', views.nomi_apply, name='nomi_apply'),

    # nominations/edit/2
    url(r'^answer_edit/(?P<pk>\d+)/$', views.nomi_answer_edit, name='nomi_answer_edit'),

    # nominations/copy_nomi_link/2
    url(r'^copy_nomi_link/(?P<pk>\d+)/$', views.copy_nomi_link, name='copy_nomi_link'),

    # nominations/profile
    url(r'^profile/$', views.profile_view, name='profile'),

    # nominations/public_profile/2
    url(r'^public_profile/(?P<pk>\d+)/$', views.public_profile, name='public_profile'),

    # nominations/profile/create
    url(r'profile/create/$', views.UserProfileCreate.as_view(), name='profile_create'),

    # nominations/profile/update/2
    url(r'^profile/update/(?P<pk>\d+)/$', views.UserProfileUpdate.as_view(), name='profile_update'),

    # nominations/applicants/2
    url(r'^applicants/(?P<pk>\d+)/$', views.applications, name='applicants'),

    # nominations/answers/2
    url(r'^answers/(?P<pk>\d+)/$', views.nomination_answer, name='nomi_answer'),

    # nominations/answers/2/comment/23
    url(r'^comment/(?P<pk>\d+)/(?P<form_pk>\d+)$', views.CommentUpdate.as_view(), name='comment_update'),
    url(r'^comment/(?P<pk>\d+)/(?P<form_pk>\d+)/delete/$', views.CommentDelete.as_view(), name='comment_delete'),

    # nominations/applicants/2 (redirect)
    url(r'^accept/(?P<pk>\d+)/$', views.accept_nomination, name='accept'),
    url(r'^reject/(?P<pk>\d+)/$', views.reject_nomination, name='reject'),
    url(r'^interviewed/(?P<pk>\d+)$', views.mark_as_interviewed, name='interviewed'),

    # nominations/append/2 (redirect)
    url(r'^append/fdybdjhhvjdk5878fkjjgj521/(?P<pk>\d+)$', views.append_user, name='append_user'),

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

    # nominations/createpost/senate/2
    url(r'^createpost/senate/(?P<pk>\d+)/$', views.senate_post_create, name='senate_post_create'),

    # nominations/post_approve/2/34
    url(r'^post_approve/(?P<post_pk>\d+)/$', views.post_approval, name='post_approval'),

    # nominations/post_reject/2/43
    url(r'^post_reject/(?P<post_pk>\d+)/$', views.post_reject, name='post_reject'),

    # nominations/post_approve/2/34
    url(r'^club_approve/(?P<club_pk>\d+)/$', views.club_approval, name='club_approval'),

    # nominations/post_reject/2/43
    url(r'^club_reject/(?P<club_pk>\d+)/$', views.club_reject, name='club_reject'),


    # nominations/child_post/2/8
    url(r'^child_post/(?P<pk>\d+)/$', views.child_post_view, name='child_post'),

    # nominations/nomi_detail/2/34/6
    url(r'^nomi_detail/(?P<nomi_pk>\d+)/$', views.nomi_detail, name='nomi_detail'),

    # nominations/post_approve/2
    url(r'^nomi_approve/(?P<nomi_pk>\d+)/$', views.nomi_approval, name='nomi_approval'),

    # nominations/nomi_reject/2
    url(r'^nomi_reject/(?P<nomi_pk>\d+)/$', views.nomi_reject, name='nomi_reject'),

    # nominations/final_nomi_approve/2/43/21
    url(r'^final_nomi_approve/(?P<nomi_pk>\d+)/$', views.final_nomi_approval, name='final_nomi_approval'),

    # nominations/re_nomi/2
    url(r'^re_nomi/(?P<nomi_pk>\d+)/$', views.reopen_nomi, name='reopen_nomi'),

    # nominations/post_approve/2
    url(r'^re_nomi_approve/(?P<re_nomi_pk>\d+)/$', views.re_nomi_approval, name='re_nomi_approval'),

    # nominations/nomi_reject/2
    url(r'^re_nomi_reject/(?P<re_nomi_pk>\d+)/$', views.re_nomi_reject, name='re_nomi_reject'),

    # nominations/final_nomi_approve/2/43/21
    url(r'^final_re_nomi_approve/(?P<re_nomi_pk>\d+)/$', views.final_re_nomi_approval, name='final_re_nomi_approval'),

    # nominations/group_nomi/2
    url(r'^group_nomi/(?P<pk>\d+)/$', views.group_nominations, name='group_nomi'),

    # nominations/result_approval/2
    url(r'^result_approval/(?P<nomi_pk>\d+)/$', views.result_approval, name='result_approval'),

    # nominations/cancel_result_approval/2
    url(r'^cancel_result_approval/(?P<nomi_pk>\d+)/$', views.cancel_result_approval, name='cancel_result_approval'),

    # nominations/ratify/2
    url(r'^ratify/(?P<nomi_pk>\d+)/$', views.ratify, name='ratify'),

    # nominations/ratify/2
    url(r'^request_ratify/(?P<nomi_pk>\d+)/$', views.request_ratify, name='request_ratify'),

    # nominations/cancel_ratify/2
    url(r'^cancel_ratify/(?P<nomi_pk>\d+)/$', views.cancel_ratify, name='cancel_ratify'),

    # nominations/group_nomi_detail/2
    url(r'^group_nomi_detail/(?P<pk>\d+)/$', views.group_nomi_detail, name='group_nomi_detail'),

    # nominations/add_to_group/2/42
    url(r'^add_to_group/(?P<pk>\d+)/(?P<gr_pk>\d+)/$', views.add_to_group, name='add_to_group'),

    # nominations/remove_from_group/2/42
    url(r'^remove_from_group/(?P<nomi_pk>\d+)/(?P<gr_pk>\d+)/$', views.remove_from_group, name='remove_from_group'),

    # nominations/remove_panelist/23/2
    url(r'^remove_panelist/(?P<nomi_pk>\d+)/(?P<user_pk>\d+)/$', views.remove_panelist, name='remove_panelist'),

    # nominations/renew
    url(r'^renew/$', views.end_tenure, name='end_tenure'),

    # nominations/ratify/2
    url(r'^request_deratify/(?P<post_pk>\d+)/(?P<user_pk>\d+)/$', views.create_deratification_request, name='request_deratify'),

    url(r'^approve_deratify/(?P<pk>\d+)/$', views.approve_deratification_request, name='approve_deratify'),

    # nominations/cancel_ratify/2
    url(r'^cancel_deratify/(?P<pk>\d+)/$', views.reject_deratification_request, name='cancel_deratify'),

]