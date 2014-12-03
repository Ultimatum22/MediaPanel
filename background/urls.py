from django.conf.urls import url, patterns

from background import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^gather_images/', views.gather_images),
                       )