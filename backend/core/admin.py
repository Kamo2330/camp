from django.contrib import admin

from .models import ContactInquiry, Industry, JobOpening, Service

admin.site.register(Service)
admin.site.register(Industry)
admin.site.register(JobOpening)
admin.site.register(ContactInquiry)
