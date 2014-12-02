from django.conf.urls import patterns, url
from panel import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'), # ex: /panel/
)