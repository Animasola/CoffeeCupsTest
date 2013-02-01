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
    priority = request.GET.get('pr', '0')
    if str(priority).isdigit() and int(priority) == 0:
        first_ten_requests = RequestsLog.objects.filter().order_by(
            'priority', 'request_timestamp')[: 10]
        toogle_sorting = 'desc'
    elif str(priority).isdigit() and int(priority) == 1:
        first_ten_requests = RequestsLog.objects.filter().order_by(
            '-priority', 'request_timestamp')[: 10]
        toogle_sorting = 'asc'
    else:
        first_ten_requests = RequestsLog.objects.filter().order_by(
            'request_timestamp')[: 10]
        toogle_sorting = 'desc'
    return {'requests': first_ten_requests, 'sorting': toogle_sorting}


def requests_change_priority(request):
    if request.method == 'POST' and request.is_ajax():
        post_dict = {}
        if 'increase' in request.POST and request.POST['increase']:
            request_object = get_object_or_None(
                RequestsLog, pk=request.POST['increase'].encode('utf-8'))
            increased_priority = request_object.priority + 1
            if increased_priority <= 2:
                request_object.priority = increased_priority
                request_object.save()
                post_dict['result'] = 'success'
                post_dict['new_value'] = increased_priority
            else:
                post_dict['result'] = 'error'
                post_dict['err_text'] = 'Already maximum priority'
        elif 'reduce' in request.POST and request.POST['reduce']:
            request_object = get_object_or_None(
                RequestsLog, pk=request.POST['reduce'].encode('utf-8'))
            reduced_priority = request_object.priority - 1
            if reduced_priority >= 0:
                request_object.priority = reduced_priority
                request_object.save()
                post_dict['result'] = 'success'
                post_dict['new_value'] = reduced_priority
            else:
                post_dict['result'] = 'error'
                post_dict['err_text'] = 'Already minimum priority'
        json = simplejson.dumps(post_dict, ensure_ascii=False)
        return HttpResponse(json, mimetype='application/json')


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
