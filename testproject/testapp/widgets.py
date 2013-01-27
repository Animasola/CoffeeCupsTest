# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


class DatePickerWidget(forms.DateInput):

    class Media:
        css = {
             'all': ("http://jquery-ui.googlecode.com/"
                    "svn/tags/latest/themes/base/jquery-ui.css",)
             }
        js = (
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.js",
            "http://ajax.googleapis.com/ajax/"
            "libs/jqueryui/1.8.1/i18n/jquery.ui.datepicker-en-GB.js")

    def __init__(self, params='', attrs=None):
        self.params = params
        super(DatePickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(DatePickerWidget, self).render(name,
                    value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
        $('#id_%s').datepicker({%s});
        </script>''' % (name, self.params, ))
