from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new_profile/$', views.new_profile, name='new_profile'),
    url(r'^new_times/$', views.new_times, name="new_times"),
    url(r'^profile/$', views.view_profile, name="view_profile"),
    url(r'^groups/$', views.groups, name="groups"),
<<<<<<< HEAD
    url(r'^groups/(?P<pk>\d+)/$', views.single_group, name="single_group"),
    url(r'^courses/(?P<department>\w+)/(?P<number>\d+)/$', views.course, name="course"),
=======
    url(r'^groups/new/$', views.create_group, name="new_group")
>>>>>>> da89fd7aca8acc7640a5e67b1d4dcf792ab7ea08
]