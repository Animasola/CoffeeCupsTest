#-*- coding:utf-8 -*-
from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from models import PersonalInfo, RequestsLog


@render_to('mainpage.html')
def show_personal_info(request):
    my_info = get_object_or_None(PersonalInfo, pk=1)
    return {'my_info': my_info}

@render_to('requests_log.html')
def requests_log_page(request):
    first_ten_requests =\
        RequestsLog.objects.filter().order_by('request_timestamp')[: 10]
    return {'requests': first_ten_requests}
