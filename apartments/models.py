from django.db import models
from django.contrib.auth.models import User


class Amenity(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji (e.g. 📶, ❄️, 🏊)")

    class Meta:
        verbose_name_plural = 'Amenities'
        ordering = ['name']

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name


class Agent(models.Model):
    """An agent who lists service apartments."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='agent_profile')
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='agents/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Short bio about the agent")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def available_count(self):
        return self.apartments.filter(status='available').count()

    @property
    def total_count(self):
        return self.apartments.count()


class Apartment(models.Model):
    """A service apartment listed by an agent."""

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, help_text="e.g. Victoria Island, Lagos")
    price = models.PositiveIntegerField(help_text="Price per night in Naira")
    bedrooms = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='apartments/', blank=True, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='apartments')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='apartments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.location}"

    @property
    def price_display(self):
        """Format price as ₦85,000"""
        return f"₦{self.price:,}"


class ApartmentImage(models.Model):
    """Multiple images for an apartment gallery."""
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='apartments/gallery/')
    caption = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.apartment.title}"


class Booking(models.Model):
    """A booking request for a service apartment."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=120)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.guest_name} - {self.apartment.title} ({self.start_date} to {self.end_date})"
