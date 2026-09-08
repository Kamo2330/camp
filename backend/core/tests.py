from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from camp.frontend_dev import can_bind_port, configure_runserver_port

from .models import ContactInquiry, Industry, Service


class ServiceModelTests(TestCase):
    def test_str_representation(self):
        service = Service.objects.create(title='Guarding', description='On-site protection')
        self.assertEqual(str(service), 'Guarding')


class SiteContentAPITests(APITestCase):
    def test_site_content_returns_brand(self):
        response = self.client.get(reverse('site-content'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], 'Camp Security')
        self.assertIn('contact', response.data)


class ServiceListAPITests(APITestCase):
    def test_list_services(self):
        Service.objects.create(title='Patrols', description='Mobile patrol units', featured=True)
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Patrols')


class ContactInquiryAPITests(APITestCase):
    def test_create_contact_inquiry(self):
        payload = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'I need a quote for event security services.',
        }
        response = self.client.post(reverse('contact-create'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactInquiry.objects.count(), 1)

    def test_rejects_short_message(self):
        payload = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Too short',
        }
        response = self.client.post(reverse('contact-create'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ApiRootTests(TestCase):
    def test_browser_is_sent_to_the_website(self):
        response = self.client.get('/', HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://localhost:3000')

    def test_api_clients_still_get_json(self):
        response = self.client.get('/', HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Camp Security API')


class HealthCheckAPITests(APITestCase):
    def test_health_check(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')


class ChatAssistantAPITests(APITestCase):
    def test_services_question(self):
        Service.objects.create(title='Event Security', description='Venue coverage')
        response = self.client.post(
            reverse('chat-assistant'),
            {'message': 'What services do you offer?', 'prefer_llm': False},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mode'], 'faq')
        self.assertIn('Camp Security', response.data['reply'])
        self.assertIn('Event Security', response.data['reply'])

    def test_contact_question(self):
        response = self.client.post(
            reverse('chat-assistant'),
            {'message': 'How can I contact you?', 'prefer_llm': False},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Email', response.data['reply'])

    def test_rejects_empty_message(self):
        response = self.client.post(
            reverse('chat-assistant'),
            {'message': ' ', 'prefer_llm': False},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Please type', response.data['reply'])


class IndustryListAPITests(APITestCase):
    def test_list_industries(self):
        Industry.objects.create(title='Retail', description='Stores and malls')
        response = self.client.get(reverse('industry-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Retail')


class RunserverPortTests(TestCase):
    def test_keeps_an_explicit_port(self):
        argv = ['manage.py', 'runserver', '9000']
        self.assertEqual(configure_runserver_port(argv), 9000)
        self.assertEqual(argv, ['manage.py', 'runserver', '9000'])

    def test_picks_a_bindable_port_when_none_given(self):
        argv = ['manage.py', 'runserver', '--noreload']
        port = configure_runserver_port(argv)
        self.assertEqual(argv[argv.index('runserver') + 1], str(port))
        self.assertIn('--noreload', argv)
        self.assertTrue(can_bind_port(port))
