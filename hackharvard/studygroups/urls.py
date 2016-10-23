from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new_profile/$', views.new_profile, name='new_profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^new_times/$', views.new_times, name="new_times"),
    url(r'^edit_times/$', views.edit_times, name="edit_times"),
    url(r'^profile/$', views.view_profile, name="view_profile"),
    url(r'^groups/$', views.groups, name="groups"),
    url(r'^groups/(?P<pk>\d+)/$', views.single_group, name="single_group"),
    url(r'^courses/(?P<department>\w+)/(?P<number>\d+)/$', views.course, name="course"),
    url(r'^groups/new/$', views.create_group, name="new_group"),
    url(r'^groups/request/(?P<pk>\d+)/$', views.request_group, name='request_group'),
    url(r'^groups/join/(?P<group_pk>\d+)/$', views.respond_invite, name='join_group'),
]