from django.conf.urls import patterns, include, url
from testapp.views import show_personal_info, requests_log_page,\
    edit_my_profile, requests_change_priority
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^$', show_personal_info, name='mainpage_url'),
    url(r'^requests/$', requests_log_page, name='requests_url'),
    url(r'^requests/priority/$', requests_change_priority, name='change_prio'),
    url(r'editinfo/', edit_my_profile, name='editinfo'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
)