from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^home_page/$', views.home_page.as_view(),
        name='home_page'),
]
