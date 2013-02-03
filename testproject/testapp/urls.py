from django.conf.urls import patterns, url
from views import show_personal_info, requests_log_page,\
    edit_my_profile, requests_change_priority


urlpatterns = patterns('',
    url(r'^$', show_personal_info, name='mainpage_url'),
    url(r'^requests/$', requests_log_page, name='requests_url'),
    url(r'^requests/priority/$', requests_change_priority, name='change_prio'),
    url(r'editinfo/', edit_my_profile, name='editinfo'),
    )