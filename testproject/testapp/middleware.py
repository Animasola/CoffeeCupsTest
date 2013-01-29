from testproject.testapp.models import RequestsLog


class RequestLogger(object):

    def process_request(self, request):
        if request.method == 'GET':
            priority_field = 0
        elif request.method == 'POST':
            priority_field = 1
        req = RequestsLog(
            requested_url=request.build_absolute_uri(request.path),
            request_type=request.method,
            request_ip=request.META['REMOTE_ADDR'],
            priority=priority_field)
        req.save()
