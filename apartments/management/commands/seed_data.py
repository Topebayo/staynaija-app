from django.core.management.base import BaseCommand
from apartments.models import Agent, Apartment


class Command(BaseCommand):
    help = 'Seed the database with sample agents and apartments'

    def handle(self, *args, **options):
        import random
        from apartments.models import Amenity, Agent, Apartment

        # Clear existing data
        Apartment.objects.all().delete()
        Agent.objects.all().delete()
        Amenity.objects.all().delete()
        self.stdout.write("Cleared existing data...")

        # Create Amenities
        amenities_data = [
            ("WiFi", "📶"), ("Air Conditioning", "❄️"), ("Swimming Pool", "🏊"),
            ("Gym", "🏋️"), ("24/7 Power", "⚡"), ("Security", "👮"),
            ("Parking", "🚗"), ("Smart TV", "📺"), ("Daily Cleaning", "🧹"),
        ]
        amenities = []
        for name, icon in amenities_data:
            amenity = Amenity.objects.create(name=name, icon=icon)
            amenities.append(amenity)
        self.stdout.write(f"  Created {len(amenities)} amenities")

        # Create agents
        agents_data = [
            {"name": "Chidi Okonkwo", "phone": "+234 801 234 5678", "email": "chidi@staynaija.com", "bio": "Top-rated agent in Lagos with 5+ years experience in luxury apartments."},
            {"name": "Amaka Eze", "phone": "+234 802 345 6789", "email": "amaka@staynaija.com", "bio": "Specializing in Ikoyi and Victoria Island premium short-lets."},
            {"name": "Tunde Bakare", "phone": "+234 803 456 7890", "email": "tunde@staynaija.com", "bio": "Your go-to agent for service apartments in Abuja."},
            {"name": "Ngozi Adeyemi", "phone": "+234 804 567 8901", "email": "ngozi@staynaija.com", "bio": "Affordable apartments in Lagos and Port Harcourt."},
            {"name": "Emeka Nwosu", "phone": "+234 805 678 9012", "email": "emeka@staynaija.com", "bio": "Luxury and executive suites across Nigeria."},
        ]

        agents = []
        for data in agents_data:
            agent = Agent.objects.create(**data)
            agents.append(agent)
            self.stdout.write(f"  Created agent: {agent.name}")

        # Create apartments
        apartments_data = [
            {"title": "Luxury 3-Bedroom Apartment", "location": "Victoria Island, Lagos", "price": 85000, "status": "available", "agent": agents[0], "bedrooms": 3, "bathrooms": 2, "description": "Stunning fully furnished apartment with ocean views, modern kitchen, and 24/7 security. Perfect for business travelers and families."},
            {"title": "Cozy Studio in Lekki", "location": "Lekki Phase 1, Lagos", "price": 35000, "status": "booked", "agent": agents[0], "bedrooms": 1, "bathrooms": 1, "description": "A warm and inviting studio perfect for solo travelers or couples visiting Lagos. Close to the mall and restaurants."},
            {"title": "Spacious 2-Bed in Ikoyi", "location": "Ikoyi, Lagos", "price": 65000, "status": "available", "agent": agents[1], "bedrooms": 2, "bathrooms": 2, "description": "Elegant apartment in the heart of Ikoyi with gym access and a rooftop pool. Walking distance to Falomo Shopping Centre."},
            {"title": "Modern Flat in Wuse", "location": "Wuse 2, Abuja", "price": 55000, "status": "available", "agent": agents[2], "bedrooms": 2, "bathrooms": 1, "description": "Centrally located modern flat close to shopping malls, restaurants, and the central business district."},
            {"title": "Executive Suite — Maitama", "location": "Maitama, Abuja", "price": 120000, "status": "booked", "agent": agents[2], "bedrooms": 4, "bathrooms": 3, "description": "Premium executive suite ideal for diplomats and business executives. Fully serviced with a dedicated concierge."},
            {"title": "Beachside Apartment", "location": "Oniru, Lagos", "price": 95000, "status": "available", "agent": agents[1], "bedrooms": 3, "bathrooms": 2, "description": "Wake up to the sound of waves in this beautiful beachside service apartment. Features a private balcony and sea views."},
            {"title": "Budget-Friendly Studio", "location": "Surulere, Lagos", "price": 20000, "status": "available", "agent": agents[3], "bedrooms": 1, "bathrooms": 1, "description": "Clean and affordable studio apartment in a quiet neighborhood. Ideal for students and budget travelers."},
            {"title": "Penthouse with City View", "location": "Eko Atlantic, Lagos", "price": 200000, "status": "booked", "agent": agents[4], "bedrooms": 5, "bathrooms": 4, "description": "Luxurious penthouse with panoramic city views, private elevator, home cinema, and concierge service."},
            {"title": "Charming 1-Bed in GRA", "location": "GRA, Port Harcourt", "price": 30000, "status": "available", "agent": agents[3], "bedrooms": 1, "bathrooms": 1, "description": "Lovely apartment in the Government Reserved Area with excellent security and close to major amenities."},
            {"title": "Family Home in Asokoro", "location": "Asokoro, Abuja", "price": 75000, "status": "available", "agent": agents[4], "bedrooms": 3, "bathrooms": 2, "description": "Spacious family-friendly apartment with a garden and kids play area. Perfect for families relocating or on vacation."},
            {"title": "Serviced Apartment in Ajah", "location": "Ajah, Lagos", "price": 28000, "status": "available", "agent": agents[0], "bedrooms": 2, "bathrooms": 1, "description": "Newly built serviced apartment with reliable power supply and water. Gated community with security."},
            {"title": "Duplex in Garki", "location": "Garki, Abuja", "price": 90000, "status": "booked", "agent": agents[2], "bedrooms": 3, "bathrooms": 3, "description": "Beautiful duplex in the Garki area of Abuja. Ideal for corporate stays and large families."},
        ]

        for data in apartments_data:
            apt = Apartment.objects.create(**data)
            # Add random amenities
            num_amenities = random.randint(3, 7)
            sampled_amenities = random.sample(amenities, num_amenities)
            apt.amenities.set(sampled_amenities)
            self.stdout.write(f"  Created: {apt.title}")

        self.stdout.write(self.style.SUCCESS(f"\nDone! Created {len(agents)} agents, {len(amenities)} amenities, and {len(apartments_data)} apartments."))
