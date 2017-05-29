from django.conf.urls import url
from . import views

app_name = 'forms'

urlpatterns = [
    # forms
    url(r'^$', views.index, name='index'),

    # forms/create
    url(r'^create/$', views.build_form, name='build_form'),

    # forms/2
    url(r'^(?P<pk>\d+)/$', views.show_form, name='show_form'),

    url(r'^creator/(?P<pk>\d+)/$', views.creator_form, name='creator_form'),

    # forms/create/ques/2
    url(r'^create/ques/(?P<pk>\d+)/$', views.add_ques, name='add_ques'),

    url(r'^update/ques/(?P<pk>\d+)/(?P<qk>\d+)/$',views.QuestionUpdate.as_view(),name='ques_update'),

    # forms/ans/2
    url(r'^ans/(?P<pk>\d+)/$', views.show_answer_form, name='ans_form'),



]