from django.conf.urls import patterns, url
from weather import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^forecast/', views.forecast),
)