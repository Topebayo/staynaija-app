from django.core.management.base import BaseCommand
from apartments.models import Apartment

# High-quality Nigerian/luxury apartment images from Unsplash
APARTMENT_IMAGES = [
    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80',  # Modern living room
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80',  # Bright apartment
    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80',  # Luxury bedroom
    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80',  # Modern house exterior
    'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',  # Luxury villa
    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',  # Modern home
    'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',  # Pool villa
    'https://images.unsplash.com/photo-1600573472550-8090b5e0745e?w=800&q=80',  # Luxurious living
    'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80',  # Modern architecture
    'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=80',  # Premium home
    'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800&q=80',  # Tropical home
    'https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&q=80',  # Interior design
]


class Command(BaseCommand):
    help = 'Add beautiful Unsplash image URLs to apartments that have no images'

    def handle(self, *args, **options):
        apartments = Apartment.objects.all()
        count = 0

        for i, apt in enumerate(apartments):
            if not apt.image and not apt.image_url:
                apt.image_url = APARTMENT_IMAGES[i % len(APARTMENT_IMAGES)]
                apt.save(update_fields=['image_url'])
                count += 1
                self.stdout.write(f'  [OK] {apt.title} - image added')

        if count == 0:
            self.stdout.write(self.style.WARNING('All apartments already have images.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Added images to {count} apartment(s)!'))
