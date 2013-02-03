from django.db import models
from django.db.models.signals import post_save, post_delete
from signals import models_change_log, moderate_comment
from django.contrib.comments.signals import comment_was_posted


class PersonalInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    last_name = models.CharField(max_length=70, verbose_name='Last Name')
    birth_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='Date of birth')
    bio = models.TextField(verbose_name='Bio')
    email = models.EmailField(max_length=75, verbose_name='Email')
    jabber = models.CharField(max_length=50, verbose_name='Jabber')
    skype = models.CharField(max_length=50, verbose_name='Skype')
    other_contacts = models.TextField(verbose_name='Other contacts')
    photo = models.ImageField(upload_to='img/', blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.last_name)


class RequestsLog(models.Model):
    requested_url = models.CharField(max_length=255)
    request_ip = models.CharField(max_length=20)
    request_type = models.CharField(max_length=10)
    request_timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    priority = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.requested_url


class DbActionsLog(models.Model):
    DELETED = 'del'
    ALTERED = 'alt'
    CREATED = 'cre'
    ACTION_CHOICES = (
        (DELETED, 'Delete'),
        (ALTERED, 'Alter'),
        (CREATED, 'Create'),)
    model_name = models.CharField(max_length=30, verbose_name='Model name')
    action = models.CharField(
        max_length=3, verbose_name='Commited action', choices=ACTION_CHOICES)
    target_instance = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Target instance')
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name='Timestamp')

    class Meta:
        verbose_name = "Database activity record"
        verbose_name_plural = "Database activity records"

    def __unicode__(self):
        return "%s %s %s %s" % (
            self.model_name, self.target_instance, self.action, self.timestamp)


comment_was_posted.connect(moderate_comment)
post_save.connect(models_change_log, dispatch_uid='create_or_update_object')
post_delete.connect(models_change_log, dispatch_uid='delete_object')
