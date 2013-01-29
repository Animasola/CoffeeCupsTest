from testproject.testapp.models import RequestsLog


class RequestLogger(object):

    def process_request(self, request):
        req = RequestsLog(
            requested_url=request.build_absolute_uri(request.path),
            request_type=request.method,
            request_ip=request.META['REMOTE_ADDR'])
        req.save()
