from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^$', views.EntryList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.EntryDetail.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)