from django.conf.urls import patterns, url
from weather import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^forecast_10_days/', views.forecast_10_days),
                       url(r'^forecast_hourly_today/', views.forecast_hourly_today),
)