import os

from django.contrib import admin
from django.conf.urls import patterns, include, url

from mediapanel import settings
from mediapanel.settings import BASE_DIR

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^', include('panel.urls')),
                       url(r'^agenda/', include('agenda.urls')),
                       url(r'^background/', include('background.urls')),
                       #url(r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += patterns('django.views.static',
                        (r'^static_media/(?P<path>.*)$',
                         'serve', {
                            'document_root': os.path.join(BASE_DIR),
                            'show_indexes': True}), )