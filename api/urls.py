from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.entry_list, name='root'),
    url(r'^documentation/$', views.documentation, name='documentation'),
    url(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.entry_detail, name='specific'),
]