from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import Context
from django.test.client import Client
from annoying.functions import get_object_or_None
from datetime import date

from models import PersonalInfo


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
        self.assertEqual(self.my_info.bio,
                    'My biography. Nothing interesting here.' * 2)
        self.assertEqual(self.my_info.email, 'annima.sola@gmail.com')
        self.assertEqual(self.my_info.jabber, 'annima@khavr.com')
        self.assertEqual(self.my_info.skype, 'gorazio1986')
        self.assertEqual(self.my_info.other_contacts, 'gorazio@ukr.net')
        self.assertEqual(self.my_info.birth_date,
                    date(1986, 12, 20))

    def test_used_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'mainpage.html')

    def test_template(self):
        self.assertContains(self.response, self.my_info.name, status_code=200)
        self.assertContains(self.response, self.my_info.last_name,
                    status_code=200)
        self.assertContains(self.response, self.my_info.bio, status_code=200)
        self.assertContains(self.response, self.my_info.email, status_code=200)
        self.assertContains(self.response, self.my_info.jabber,
                    status_code=200)
        self.assertContains(self.response, self.my_info.skype, status_code=200)
        self.assertContains(self.response, self.my_info.other_contacts,
                    status_code=200)

    def test_context(self):
        self.assertTrue('my_info' in self.response.context)
        self.assertTrue(self.my_info.name in\
                    str(self.response.context['my_info']))
        self.assertTrue(self.my_info.last_name in\
         str(self.response.context['my_info']))