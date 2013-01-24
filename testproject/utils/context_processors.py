#-*- coding:utf-8 -*-
from django.conf import settings as djset


def django_settings(request):
    return {'django_settings': djset}
