from django.conf.urls import url
from . import views

urlpatterns = [
    # nominations/
    url(r'^$', views.index, name='index'),

    # nominations/2
    url(r'^(?P<pk>\d+)/$', views.nomi_apply, name='nomi_apply'),

    # nominations/result
    url(r'^result/$', views.ResultView.as_view(), name='result')

]