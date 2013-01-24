from django import forms
from django.forms import ModelForm

from models import PersonalInfo


class PersonalInfoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)

    class Media:
        js = ("http://code.jquery.com/jquery-latest.js",)

    class Meta:
        model = PersonalInfo
