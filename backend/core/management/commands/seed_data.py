from django.core.management.base import BaseCommand

from core.models import Industry, JobOpening, Service


class Command(BaseCommand):
    help = 'Seed the database with Camp Security demo content'

    def handle(self, *args, **options):
        services = [
            ('Professional Guarding', 'Vetted, trained, and supervised guards on-site 24/7.', True, 1),
            ('Mobile Patrols', 'Visible deterrence with rapid response capability.', True, 2),
            ('CCTV & Monitoring', 'Proactive surveillance with incident reporting.', True, 3),
            ('Event Security', 'Crowd management and VIP protection for any size event.', True, 4),
            ('Guarding', 'Armed and unarmed guards, access control, visitor management.', False, 5),
            ('Patrols', 'Marked vehicle patrols and perimeter inspections.', False, 6),
            ('CCTV', 'Installation, monitoring, and incident escalation.', False, 7),
            ('Armed Response', 'Rapid response and alarm verification.', False, 8),
            ('Consulting', 'Risk assessments, SOPs, emergency planning, and training.', False, 9),
        ]
        for title, description, featured, order in services:
            Service.objects.update_or_create(
                title=title,
                defaults={'description': description, 'featured': featured, 'order': order},
            )

        industries = [
            ('Corporate', 'Head offices, business parks, and logistics facilities.', 1),
            ('Retail', 'Shopping centres, supermarkets, and high-street stores.', 2),
            ('Healthcare', 'Hospitals and clinics with sensitive environments.', 3),
            ('Education', 'Schools and campuses requiring safe learning spaces.', 4),
            ('Residential', 'Gated estates and apartment complexes.', 5),
        ]
        for title, description, order in industries:
            Industry.objects.update_or_create(
                title=title,
                defaults={'description': description, 'order': order},
            )

        jobs = [
            ('Security Officers (Armed/Unarmed)', 1),
            ('Supervisors', 2),
            ('Mobile Patrol Officers', 3),
            ('Event Security', 4),
        ]
        for title, order in jobs:
            JobOpening.objects.update_or_create(title=title, defaults={'order': order})

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
