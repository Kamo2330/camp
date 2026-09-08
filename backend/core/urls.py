from django.urls import path

from .views import (
    ChatAssistantView,
    ContactInquiryCreateView,
    HealthCheckView,
    IndustryListView,
    JobOpeningListView,
    ServiceListView,
    SiteContentView,
)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('site/', SiteContentView.as_view(), name='site-content'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('industries/', IndustryListView.as_view(), name='industry-list'),
    path('jobs/', JobOpeningListView.as_view(), name='job-list'),
    path('contact/', ContactInquiryCreateView.as_view(), name='contact-create'),
    path('chat/', ChatAssistantView.as_view(), name='chat-assistant'),
]
