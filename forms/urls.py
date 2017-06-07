from django.conf.urls import url
from . import views

app_name = 'forms'

urlpatterns = [


    #forms/creator/12 ----in great use
    url(r'^creator/(?P<pk>\d+)/$', views.creator_form, name='creator_form'),

    # forms/create/ques/2  ---in use
    url(r'^create/ques/(?P<pk>\d+)/$', views.add_ques, name='add_ques'),

    # forms/update/ques/12/34 ---in use
    url(r'^update/ques/(?P<pk>\d+)/(?P<qk>\d+)/$',views.QuestionUpdate.as_view(),name='ques_update'),

    # forms---not in use
    url(r'^$', views.index, name='index'),

    # forms/create---- not in project use
    url(r'^create/$', views.build_form, name='build_form'),

    # forms/2 ----not in project use
    url(r'^(?P<pk>\d+)/$', views.show_form, name='show_form'),

    # forms/ans/2   ---not in use
    url(r'^ans/(?P<pk>\d+)/$', views.show_answer_form, name='ans_form'),



]