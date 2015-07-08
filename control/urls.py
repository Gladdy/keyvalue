from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^settings/$', views.settings, name='settings'),
]