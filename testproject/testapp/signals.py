# -*- coding: utf-8 -*-
from django.conf import settings
import logging
import pprint
import traceback
import os
from django.utils.encoding import smart_str
from django.core.mail import send_mail
import akismet
from django.conf import settings
from django.contrib.sites.models import Site

from models import PersonalInfo


logging.basicConfig(
    level=logging.ERROR,
    filename=os.path.join(settings.DEPLOY_DIR, 'signals.log'),
    filemode='w')


def models_change_log(sender, instance, signal, *args, **kwargs):
    model = sender.__name__
    if model == 'DbActionsLog':
        return
    targt_instance = instance
    from models import DbActionsLog
    if 'created' in kwargs:
        if kwargs['created']:
            action_ = DbActionsLog.CREATED
        else:
            action_ = DbActionsLog.ALTERED
    else:
        action_ = DbActionsLog.DELETED
    log_record = DbActionsLog(
        model_name=model,
        target_instance=targt_instance,
        action=action_,)
    try:
        log_record.save()
    except:
        stack = pprint.pformat(traceback.extract_stack())
        logging.error('An error occurred:\n %s' % stack)


def moderate_comment(sender, comment, request, **kwargs):
    ak = akismet.Akismet(
        key = settings.AKISMET_API_KEY,
        blog_url = 'http://%s/' % Site.objects.get_current().domain)
    data = {
        'user_ip': request.META.get('REMOTE_ADDR', ''),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'referrer': request.META.get('HTTP_REFERRER', ''),
        'comment_type': 'comment',
        'comment_author': smart_str(comment.user_name),}
    if ak.comment_check(
        smart_str(comment.comment), data=data, build_data=True):
        comment.is_public = False
        comment.save()
    if comment.is_public:
        my_email = PersonalInfo.objects.get(pk=1).email
        email_body = "%s"
        send_mail(
            "New contact request!",
            '%s' % comment.get_as_text(),
            'andrew.rovno@gmail.com',
            [my_email],
            fail_silently=False)
