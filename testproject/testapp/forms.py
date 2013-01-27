from django import forms
from django.conf import settings
from django.forms import ModelForm

from models import PersonalInfo
from widgets import DatePickerWidget


class PersonalInfoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs["onchange"] = "upload_img(this);"
        self.fields['birth_date'].widget = DatePickerWidget(
            params="dateFormat: 'yy-mm-dd', changeYear: true,"
            " defaultDate: '-16y', yearRange: 'c-40:c+16'",
            attrs={'class': 'datepicker', })

    class Media:
        js = (
            "/static/js/jquery.form_3.09.js",
            '%sjs/photo_preview.js' % settings.STATIC_URL,)

    class Meta:
        model = PersonalInfo
