from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', 'todo.views.user_login', name='user_login'),
    url(r'^accounts/logout/', 'todo.views.user_logout', name='user_logout'),
    url(r'^accounts/register/', 'todo.views.user_register', name='user_register'),
    url(r'^', include('website.urls', namespace='website'))
)
