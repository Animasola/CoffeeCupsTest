from django.contrib import admin
from models import PersonalInfo, RequestsLog, DbActionsLog


class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'last_name', 'birth_date',
        'email', 'skype', 'jabber', 'other_contacts',)
    search_fields = ['last_name', 'name']


class RequestsLogAdmin(admin.ModelAdmin):
    list_display = (
        'requested_url', 'request_ip', 'request_type', 'request_timestamp',)
    search_field = ['requested_url']
    list_filter = ('request_type',)
    date_hierarchy = 'request_timestamp'


class DbActionsLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'target_instance', 'action', 'timestamp', )
    list_filter = ('model_name', 'action',)
    date_hierarchy = 'timestamp'
    search_fields = ['model']

admin.site.register(PersonalInfo, PersonalInfoAdmin)
admin.site.register(RequestsLog, RequestsLogAdmin)
admin.site.register(DbActionsLog, DbActionsLogAdmin)
