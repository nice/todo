from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^task/$', 'website.views.task', name='task'),
    url(r'^task/(?P<task_id>\d+)/$', 'website.views.task', name='task'),
    url(r'^view-task/$', 'website.views.view_task', name='view_task'),
    url(r'^update-task/(?P<item>[^/]+)/$', 'website.views.update_task', name='update_task'),
    url(r'^delete-task/$', 'website.views.delete_task', name='delete_task'),
    url(r'^filter/(?P<target>[^/]+)/$', 'website.views.filter', name='filter'),
    # fallback url :)
    url(r'^.*', 'website.views.index'),
)
