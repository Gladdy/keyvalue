from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.entry_list),
    url(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.entry_detail),
]