from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new_profile/$', views.new_profile, name='new_profile'),
    url(r'^new_times/$', views.new_times, name="new_times"),
    url(r'^profile/$', views.view_profile, name="view_profile"),
    url(r'^groups/$', views.groups, name="groups"),
    url(r'^groups/(?P<pk>\d+)/$', views.single_group, name="single_group"),
    url(r'^courses/(?P<department>\w+)/(?P<number>\d+)/$', views.course, name="course"),
]