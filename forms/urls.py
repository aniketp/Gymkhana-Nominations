from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index1'),
    url(r'^create/$', views.build_form, name='build_form'),
    url(r'^(?P<pk>\d+)/$', views.show_form, name='show_form'),
    url(r'^create/ques/(?P<pk>\d+)/$', views.add_ques, name='add_ques'),

]