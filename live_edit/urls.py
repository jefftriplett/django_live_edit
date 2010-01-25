from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$',
        view='live_edit.views.live_edit',
        name='live_edit'),

    url(r'^form/(?P<app_label>[-\w]+)/(?P<module_label>[-\w]+)/(?P<field>[-\w]+)/$',
        view='live_edit.views.live_edit_form',
        name='live_edit_form'),

    url(r'^json/(?P<app_label>[-\w]+)/(?P<module_label>[-\w]+)/(?P<field>[-\w]+)/$',
        view='live_edit.views.live_edit_json',
        name='live_edit_json'),
)
