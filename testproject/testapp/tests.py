from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import Context
from django.test.client import Client
from annoying.functions import get_object_or_None
from django_any import any_model
from datetime import date

from models import PersonalInfo, RequestsLog


class MainPageTest(TestCase):
    fixtures = ['initial_date.json']

    def setUp(self):
        self.my_info = get_object_or_None(PersonalInfo, pk=1)
        self.client = Client()
        self.response = self.client.get(reverse('mainpage_url'))

    def test_object_as_string(self):
        self.assertEqual(str(self.my_info), 'Andrew Gordiychuk')

    def test_models_fields(self):
        self.assertEqual(self.my_info.name, 'Andrew')
        self.assertEqual(self.my_info.last_name, 'Gordiychuk')
        self.assertEqual(
            self.my_info.bio, 'My biography. Nothing interesting here.' * 2)
        self.assertEqual(self.my_info.email, 'annima.sola@gmail.com')
        self.assertEqual(self.my_info.jabber, 'annima@khavr.com')
        self.assertEqual(self.my_info.skype, 'gorazio1986')
        self.assertEqual(self.my_info.other_contacts, 'gorazio@ukr.net')
        self.assertEqual(self.my_info.birth_date, date(1986, 12, 20))

    def test_used_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'mainpage.html')

    def test_template(self):
        self.assertContains(self.response, self.my_info.name, status_code=200)
        self.assertContains(
            self.response, self.my_info.last_name, status_code=200)
        self.assertContains(self.response, self.my_info.bio, status_code=200)
        self.assertContains(self.response, self.my_info.email, status_code=200)
        self.assertContains(
            self.response, self.my_info.jabber, status_code=200)
        self.assertContains(self.response, self.my_info.skype, status_code=200)
        self.assertContains(
            self.response, self.my_info.other_contacts, status_code=200)

    def test_context(self):
        self.assertTrue('my_info' in self.response.context)
        self.assertTrue(
            self.my_info.name in str(self.response.context['my_info']))
        self.assertTrue(
            self.my_info.last_name in str(self.response.context['my_info']))


class RequestsLogTemplateTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_template(self):
        response = self.client.get(reverse('requests_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests_log.html')

    def test_requests_page(self):
        response = self.client.get(reverse('requests_url'))
        self.assertContains(response, 'from', count=1, status_code=200)
        for n in xrange(15):
            response = self.client.get(reverse('requests_url'))
        self.assertContains(response, 'from', count=10, status_code=200)

    def test_template_context(self):
        response = self.client.get(reverse('requests_url'))
        self.assertTrue('requests' in response.context)
        requestslog_object = RequestsLog.objects.get(pk=1)
        self.assertContains(
            response, requestslog_object.requested_url, status_code=200)
        self.assertContains(
            response, requestslog_object.request_type, status_code=200)
        self.assertContains(
            response, requestslog_object.request_ip, status_code=200)


class RequestsLogModelTest(TestCase):

    def setUp(self):
        self.new_request = any_model(RequestsLog)

    def test_save_object(self):
        self.new_request.save()
        requestslog_object = RequestsLog.objects.get(
            request_timestamp=self.new_request.request_timestamp)
        self.assertEqual(
            requestslog_object.requested_url, self.new_request.requested_url)
        self.assertEqual(
            requestslog_object.request_type, self.new_request.request_type)

    def test_delete_object(self):
        self.new_request.delete()
        requestslog_object = get_object_or_None(
            RequestsLog, request_timestamp=self.new_request.request_timestamp)
        self.assertTrue(requestslog_object is None)
