from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$',
        view='live_edit.views.live_edit',
        name='live_edit'),

    url(r'^form/$',
        view='live_edit.views.live_edit_form',
        name='live_edit'),

    url(r'^json/$',
        view='live_edit.views.live_edit_json',
        name='live_edit_json'),

    url(r'^snippet/$',
        view='live_edit.views.live_edit_snippet',
        name='live_edit_snippet'),
)
