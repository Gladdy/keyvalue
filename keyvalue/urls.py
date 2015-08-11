from django.conf.urls import include, url
from django.contrib import admin


from . import views

urlpatterns = [
    url(r'^$', views.index, name="index-index"),

    url(r'^features/$', views.features, name="index-features"),
    url(r'^about/$', views.about, name="index-about"),
    url(r'^documentation/$', views.documentation, name='documentation'),

    url(r'^control/', include('control.urls', namespace="control")),
    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


