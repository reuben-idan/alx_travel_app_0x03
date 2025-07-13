from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        sample_titles = [
            "Ocean View Apartment", "Cozy Mountain Cabin",
            "City Center Studio", "Luxury Villa", "Budget Room"
        ]
        Listing.objects.all().delete()
        for _ in range(10):
            Listing.objects.create(
                title=random.choice(sample_titles),
                description="Lorem ipsum dolor sit amet.",
                price_per_night=random.uniform(50, 300),
                location=random.choice(["Accra", "Tema", "Kumasi", "Cape Coast"])
            )
        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
