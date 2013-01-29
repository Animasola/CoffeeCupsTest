#-*- coding:utf-8 -*-
from annoying.decorators import render_to
from django.views.generic.simple import direct_to_template
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.http import HttpResponse

from models import PersonalInfo, RequestsLog
from forms import PersonalInfoForm


@render_to('mainpage.html')
def show_personal_info(request):
    my_info = get_object_or_None(PersonalInfo, pk=1)
    return {'my_info': my_info}


@render_to('requests_log.html')
def requests_log_page(request):
    try:
        priority = request.GET['pr'].encode('utf-8')
    except:
        priority = '0'
    if int(priority) == 0:
        first_ten_requests = RequestsLog.objects.filter().order_by(
            'priority', 'request_timestamp')[: 10]
    elif int(priority) == 1:
        first_ten_requests = RequestsLog.objects.filter().order_by(
            '-priority', 'request_timestamp')[: 10]
    return {'requests': first_ten_requests}


@login_required
def edit_my_profile(request):
    my_info = get_object_or_None(PersonalInfo, pk=1)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=my_info)
        response_dict = {}
        if request.is_ajax():
            if form.is_valid():
                form.save()
                response_dict['result'] = 'success'
            else:
                response_dict['result'] = 'error'
                errors = {}
                for error in form.errors:
                    errors[error] = form.errors[error][0]
                response_dict['form_errors'] = errors
            json = simplejson.dumps(response_dict, ensure_ascii=False)
            return HttpResponse(json, mimetype='application/json')
        else:
            if form.is_valid():
                form.save()
                return redirect(reverse('mainpage_url'))
    else:
        form = PersonalInfoForm(instance=my_info)
    return direct_to_template(
        request, 'profile_edit.html', {'form': form, 'photo': my_info.photo})
