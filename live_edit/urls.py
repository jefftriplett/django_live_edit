from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$', view='live_edit.views.live_edit', name='live_edit'),
)
