from django.conf.urls import url, patterns

from agenda import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       )