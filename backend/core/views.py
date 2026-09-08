from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .chat import get_reply
from .models import ContactInquiry, Industry, JobOpening, Service
from .serializers import (
    ContactInquirySerializer,
    IndustrySerializer,
    JobOpeningSerializer,
    ServiceSerializer,
)

CAREER_BENEFITS = [
    'Competitive pay',
    'Training and certification',
    'Career progression',
    'Supportive leadership',
]

ABOUT_SECTIONS = [
    {
        'title': 'Mission',
        'description': 'Protect people and property with professionalism, integrity, and vigilance.',
    },
    {
        'title': 'Certifications',
        'description': 'PSIRA registered, first-aid certified, and continuous training compliance.',
    },
    {
        'title': 'Our Team',
        'description': 'Experienced leadership and trained officers serving 24/7.',
    },
]


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class IndustryListView(generics.ListAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer


class JobOpeningListView(generics.ListAPIView):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer


class ContactInquiryCreateView(generics.CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer


class SiteContentView(APIView):
    """Aggregated site content for the frontend."""

    def get(self, request):
        services = ServiceSerializer(Service.objects.filter(featured=True), many=True).data
        return Response(
            {
                'brand': 'Camp Security',
                'home': {
                    'eyebrow': 'Security you can trust',
                    'title': 'Welcome to Camp Security',
                    'subtitle': 'Trusted security services for your people, property, and peace of mind.',
                    'featured_services': services,
                },
                'about': {
                    'eyebrow': 'Who we are',
                    'title': 'About Camp Security',
                    'subtitle': 'Your trusted partner for comprehensive security solutions.',
                    'sections': ABOUT_SECTIONS,
                },
                'services_page': {
                    'eyebrow': 'What we do',
                    'title': 'Our Security Services',
                    'subtitle': 'Tailored protection for businesses, estates, and events.',
                },
                'clients_page': {
                    'eyebrow': 'Trusted by many',
                    'title': 'Our Clients',
                    'subtitle': 'Reliable protection across industries.',
                    'testimonial': 'Professional and reliable — our first choice for security.',
                },
                'careers_page': {
                    'eyebrow': 'Work with us',
                    'title': 'Join Our Team',
                    'subtitle': 'Grow your career with Camp Security.',
                    'benefits': CAREER_BENEFITS,
                },
                'contact_page': {
                    'eyebrow': 'Get in touch',
                    'title': 'Contact Us',
                    'subtitle': 'We respond promptly to all inquiries.',
                },
                'contact': {
                    'phone_emergency': '(555) 911-SECURITY',
                    'phone_office': '(555) 123-SECURE',
                    'email_info': settings.CONTACT_EMAIL,
                    'email_sales': settings.SALES_EMAIL,
                    'email_careers': settings.CAREERS_EMAIL,
                    'address': '123 Security Plaza, Business District',
                },
            }
        )


class HealthCheckView(APIView):
    def get(self, request):
        return Response({'status': 'ok', 'service': 'camp-api'})


class ChatAssistantView(APIView):
    """Site chat assistant (FAQ by default; LLM if GROQ_API_KEY / OPENAI_API_KEY is set)."""

    def post(self, request):
        message = request.data.get('message', '')
        if not isinstance(message, str):
            return Response(
                {'detail': 'message must be a string'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        prefer_llm = request.data.get('prefer_llm', True)
        result = get_reply(message, prefer_llm=bool(prefer_llm))
        return Response(result)
