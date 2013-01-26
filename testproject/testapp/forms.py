from django import forms
from django.conf import settings
from django.forms import ModelForm

from models import PersonalInfo


class PersonalInfoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs["onchange"] = "upload_img(this);"

    class Media:
        js = (
            "http://code.jquery.com/jquery-latest.js",
            '%sjs/photo_preview.js' % settings.STATIC_URL,)

    class Meta:
        model = PersonalInfo
