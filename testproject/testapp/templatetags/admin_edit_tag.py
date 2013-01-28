# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_in_admin(context, parse_me):
    try:
        content_type = ContentType.objects.get_for_model(parse_me)
        url = reverse(
            'admin:%s_%s_change' % (str(content_type.app_label),
            str(content_type.model)),
            args=(parse_me.id,))
        return url
    except template.VariableDoesNotExist:
        return ''
