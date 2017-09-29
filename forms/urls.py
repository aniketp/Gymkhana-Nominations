from django.conf.urls import url
from . import views

app_name = 'forms'

urlpatterns = [


    #forms/creator/12 ----in great use
    url(r'^creator/(?P<pk>\d+)/$', views.creator_form, name='creator_form'),

    # forms/create/ques/2  ---in use
    url(r'^create/ques/(?P<pk>\d+)/$', views.add_ques, name='add_ques'),

    # forms/update/ques/12/34 ---in use
    url(r'^update/ques/(?P<pk>\d+)/(?P<qk>\d+)/$',views.edit_ques,name='ques_update'),


]