#-*- coding:utf-8 -*-
from annoying.decorators import render_to
from django.views.generic.simple import direct_to_template
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required

from models import PersonalInfo, RequestsLog
from forms import PersonalInfoForm


@render_to('mainpage.html')
def show_personal_info(request):
    my_info = get_object_or_None(PersonalInfo, pk=1)
    return {'my_info': my_info}


@render_to('requests_log.html')
def requests_log_page(request):
    first_ten_requests =\
        RequestsLog.objects.filter().order_by('request_timestamp')[: 10]
    return {'requests': first_ten_requests}


@login_required
def edit_my_profile(request):
    my_info = get_object_or_None(PersonalInfo, pk=1)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=my_info)
        if form.is_valid():
            form.save()
    else:
        form = PersonalInfoForm(instance=my_info)
    return direct_to_template(request, 'profile_edit.html', {'form': form})
