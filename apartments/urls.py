from django.urls import path
from . import views

app_name = 'apartments'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('apartment/<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('agent/<int:pk>/', views.agent_detail, name='agent_detail'),

    # Authentication
    path('signup/', views.agent_signup, name='signup'),
    path('login/', views.agent_login, name='login'),
    path('logout/', views.agent_logout, name='logout'),

    # Agent Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add/', views.add_apartment, name='add_apartment'),
    path('dashboard/edit/<int:pk>/', views.edit_apartment, name='edit_apartment'),
    path('dashboard/delete/<int:pk>/', views.delete_apartment, name='delete_apartment'),
    path('dashboard/profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/bookings/', views.agent_bookings, name='agent_bookings'),
    path('dashboard/bookings/<int:pk>/status/<str:status>/', views.update_booking_status, name='update_booking_status'),
]
