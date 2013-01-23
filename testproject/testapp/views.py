#-*- coding:utf-8 -*-
from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from models import PersonalInfo


@render_to('mainpage.html')
def show_personal_info(request):
    my_info = get_object_or_None(PersonalInfo, pk=1)
    return {'my_info': my_info}
