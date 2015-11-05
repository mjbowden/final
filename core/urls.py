from django.conf.urls import patterns, unclude, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
)