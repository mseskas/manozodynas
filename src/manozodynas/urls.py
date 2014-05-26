from django.conf.urls import patterns, url
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import *

urlpatterns = patterns('',
    url(r'^$', main_view, kwargs={'word_id':-1}, name='index'),
    url(r'^(?P<word_id>\d+)/$', main_view, name='wordId'),
    url(r'^word$', word_view, name='word'),

 
    url(r'^login$', login_view, name='login'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
