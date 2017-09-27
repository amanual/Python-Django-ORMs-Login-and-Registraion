from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^show$', views.show),
    url(r'^login$', views.login),
    url(r'^remove/(?P<id>\d+)$', views.remove)
    
]