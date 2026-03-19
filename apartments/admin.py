from django.contrib import admin
from .models import Agent, Apartment, Booking, Amenity, ApartmentImage


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'available_count', 'total_count')
    search_fields = ('name', 'email')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 1

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_display', 'status', 'agent', 'bedrooms')
    list_filter = ('status', 'agent', 'location', 'amenities')
    search_fields = ('title', 'location', 'agent__name')
    list_editable = ('status',)
    inlines = [ApartmentImageInline]
    filter_horizontal = ('amenities',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'apartment', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'apartment')
    search_fields = ('guest_name', 'guest_email', 'apartment__title')
    list_editable = ('status',)
