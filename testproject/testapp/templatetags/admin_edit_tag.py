# -*- coding: utf-8 -*-
from django import template
from django.template import Variable, Node
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()


def get_url(parser, token):
    try:
        tag_name, some_object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly one argument" % token.contents.split()[0])
    return changeLink(some_object)


class changeLink(Node):
    def __init__(self, some_object):
        self.some_object = template.Variable(some_object)

    def render(self, context):
        try:
            object_to_edit = self.some_object.resolve(context)
            content_type = ContentType.objects.get_for_model(object_to_edit)
            url = reverse(
                'admin:' + str(
                    content_type.app_label) + '_' + str(
                        content_type.model + '_change'), args=(
                            object_to_edit.id,))
            return url
        except template.VariableDoesNotExist:
            return ''

register.tag('admin_url', get_url)
