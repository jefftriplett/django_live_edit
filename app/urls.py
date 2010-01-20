from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('')

urlpatterns += patterns('',
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True} ),
)

urlpatterns += patterns('',
    url(r'^entry/(?P<id>\d+)/$', view='app.views.entry_detail', name='entry_detail'),
    url(r'^live_edit/', include('live_edit.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
