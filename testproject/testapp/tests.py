from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import Template
from django.template import Context
from django.test.client import Client
from annoying.functions import get_object_or_None
from django_any import any_model
from django.db.models import get_models
from StringIO import StringIO
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from datetime import date, datetime

from models import PersonalInfo, RequestsLog
from forms import PersonalInfoForm


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


class ContextProcessorTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_template_context(self):
        response = self.client.get(reverse('mainpage_url'))
        self.assertTrue('django_settings' in response.context)
        django_settings = response.context['django_settings']
        self.assertTrue(isinstance(django_settings, type(settings)))
        self.assertEquals(django_settings.ROOT_URLCONF, 'testproject.urls')


class FormValidationTest(TestCase):
    fixtures = ['initial_date.json']

    def setUp(self):
        self.current_instance = get_object_or_None(PersonalInfo, pk=1)
        self.file_obj = StringIO()
        self.image = Image.new("RGBA", size=(40, 60), color=(256, 239, 114))
        self.image.save(self.file_obj, 'png')
        self.file_obj.name = 'test_%s.png' % datetime.now().microsecond
        self.file_obj.seek(0)
        self.form_data = any_model(PersonalInfo, photo="")
        self.post_dict = {
            'name': self.form_data.name,
            'last_name': self.form_data.last_name,
            'email': self.form_data.email,
            'jabber': self.form_data.jabber,
            'skype': self.form_data.skype,
            'bio': self.form_data.bio[0],
            'other_contacts': self.form_data.other_contacts[0],
            'birth_date': self.form_data.birth_date}

    def test_edit_profile_view(self):
        response = self.client.get(reverse('editinfo'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            response['Location'],
            'http://testserver%s?next=%s' % (
                reverse('login'), reverse('editinfo')))
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('editinfo'))
        self.assertEquals(response.status_code, 200)

    def test_form(self):
        file_dict = {
            'photo': SimpleUploadedFile(
                self.file_obj.name, self.file_obj.read())}
        self.assertTrue(self.current_instance is not None)
        form = PersonalInfoForm(
            self.post_dict, file_dict, instance=self.current_instance)
        self.assertTrue(form.is_valid())
        form.save()
        response = self.client.get(reverse('mainpage_url'))
        for key, value in self.post_dict.iteritems():
            if key == 'birth_date':
                value = value.strftime('%B %m, %Y')
                self.assertContains(response, value, status_code=200)
            else:
                self.assertContains(response, value, status_code=200)

    def test_edit_profile_view_ajax(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(
            reverse('editinfo'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])
        #with no data
        self.assertContains(response, 'error')
        response = self.client.post(
            reverse('editinfo'),
            self.post_dict,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        #with data
        self.assertNotContains(response, 'error')


class TemplateTagTest(TestCase):

    def setUp(self):
        self.current_instance = get_object_or_None(PersonalInfo, pk=1)
        self.client = Client()

    def test_templatetag(self):
        template = Template(
            '{% load admin_edit_tag %}{% get_in_admin object %}')
        context = Context({"object": self.current_instance})
        url = u'/admin/testapp/personalinfo/1/'
        self.failUnlessEqual(url, template.render(context))
        response = self.client.get(template.render(context))
        self.assertEquals(response.status_code, 200)


class CommandTest(TestCase):

    def setUp(self):
        self.err = StringIO()
        self.out = StringIO()

    def test_command(self):
        call_command("models_info", stderr=self.err, stdout=self.out)
        self.err.seek(0)
        self.out.seek(0)
        err_list = self.err.read().splitlines()
        out_list = self.out.read().splitlines()
        for model in get_models():
            #stderr must contains this line
            err_line = "error: [%s] - %s objects" % (
                model.__name__,
                model._default_manager.count())
            self.assertTrue(err_line in err_list)
            #stdout must contains this line
            out_line = "[%s] - %s objects" % (
                model.__name__,
                model._default_manager.count())
            self.assertTrue(out_line in out_list)
        self.assertEquals(len(get_models()), len(out_list))
        self.assertEquals(len(get_models()), len(err_list))
