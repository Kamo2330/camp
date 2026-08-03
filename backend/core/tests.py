from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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


class HealthCheckAPITests(APITestCase):
    def test_health_check(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')


class IndustryListAPITests(APITestCase):
    def test_list_industries(self):
        Industry.objects.create(title='Retail', description='Stores and malls')
        response = self.client.get(reverse('industry-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
