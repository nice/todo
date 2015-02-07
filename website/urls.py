from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^new-task/$', 'website.views.new_task', name='new_task'),
    url(r'^update-task/(?P<item>[^/]+)/$', 'website.views.update_task', name='update_task'),
    url(r'^view-task/$', 'website.views.view_task', name='view_task'),
)
