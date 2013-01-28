# -*- coding: utf-8 -*-
from django.db.models import get_models
from django.conf import settings
import logging
import pprint
import traceback
import os


logging.basicConfig(
    level=logging.ERROR,
    filename=os.path.join(settings.DEPLOY_DIR, 'signals.log'),
    filemode='w')


def models_change_log(sender, instance, signal, *args, **kwargs):
    model = sender.__name__
    if model == 'DbActionsLog':
        return
    targt_instance = instance
    if 'created' in kwargs:
        if kwargs['created']:
            action_ = "Created"
        else:
            action_ = "Altered"
    else:
        action_ = "Deleted"
    from models import DbActionsLog
    log_record = DbActionsLog(
        model_name=model,
        target_instance=targt_instance,
        action=action_,)
    try:
        log_record.save()
    except:
        stack = pprint.pformat(traceback.extract_stack())
        logging.error('An error occurred:\n %s' % stack)
