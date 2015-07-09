from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Management
    url(r'^values/$', views.values, name='values'),
    url(r'^manual/$', views.manual, name='manual'),
    url(r'^bulk/$', views.bulk, name='bulk'),
    url(r'^apikeys/$', views.apikeys, name='apikeys'),

    # Settings
    url(r'^restrictions/$', views.restrictions, name='restrictions'),

    # Form submits
    url(r'^generate_apikey/$', views.generate_apikey, name='generate_apikey'),
    url(r'^delete_apikey/$', views.delete_apikey, name='delete_apikey'),
]