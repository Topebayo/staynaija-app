from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Apartment, Agent, Booking, Amenity, ApartmentImage
from .forms import AgentSignupForm, LoginForm, ApartmentForm, AgentProfileForm, BookingForm


def home(request):
    """Homepage — show all apartments with search & filter."""
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    bedrooms = request.GET.get('bedrooms', '').strip()

    apartments = Apartment.objects.select_related('agent').prefetch_related('amenities').all()

    # Search by agent name, location, or title
    if query:
        apartments = apartments.filter(
            Q(agent__name__icontains=query) |
            Q(location__icontains=query) |
            Q(title__icontains=query)
        )

    # Advanced Filters
    if status_filter in ('available', 'booked'):
        apartments = apartments.filter(status=status_filter)
        
    if min_price and min_price.isdigit():
        apartments = apartments.filter(price__gte=int(min_price))
        
    if max_price and max_price.isdigit():
        apartments = apartments.filter(price__lte=int(max_price))
        
    if bedrooms and bedrooms.isdigit():
        apartments = apartments.filter(bedrooms__gte=int(bedrooms))

    # Pagination
    paginator = Paginator(apartments, 9) # 9 apartments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Stats for the hero section
    total = Apartment.objects.count()
    available = Apartment.objects.filter(status='available').count()
    agents_count = Agent.objects.count()

    context = {
        'apartments': page_obj,
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'total': total,
        'available': available,
        'agents_count': agents_count,
    }
    return render(request, 'home.html', context)


def apartment_detail(request, pk):
    """Detail page for a single apartment."""
    apartment = get_object_or_404(Apartment.objects.select_related('agent').prefetch_related('gallery_images', 'amenities'), pk=pk)
    related = apartment.agent.apartments.exclude(pk=pk)[:3]
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.apartment = apartment
            booking.save()
            messages.success(request, f"Booking request sent successfully to {apartment.agent.name}!")
            return redirect('apartments:apartment_detail', pk=apartment.pk)
    else:
        form = BookingForm()

    context = {
        'apartment': apartment,
        'related': related,
        'form': form,
    }
    return render(request, 'apartment_detail.html', context)


def agent_detail(request, pk):
    """All apartments by a specific agent."""
    agent = get_object_or_404(Agent, pk=pk)
    apartments = agent.apartments.all()
    context = {
        'agent': agent,
        'apartments': apartments,
    }
    return render(request, 'agent_detail.html', context)


# ─── Authentication ─────────────────────────────────────────────

def agent_signup(request):
    """Register a new agent account."""
    if request.user.is_authenticated:
        return redirect('apartments:dashboard')

    if request.method == 'POST':
        form = AgentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {form.cleaned_data['name']}! Your agent account is ready.")
            return redirect('apartments:dashboard')
    else:
        form = AgentSignupForm()

    return render(request, 'auth/signup.html', {'form': form})


def agent_login(request):
    """Log in an existing agent."""
    if request.user.is_authenticated:
        return redirect('apartments:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                next_url = request.GET.get('next', 'apartments:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def agent_logout(request):
    """Log out the current agent."""
    logout(request)
    messages.info(request, "You've been logged out.")
    return redirect('apartments:home')


# ─── Agent Dashboard ────────────────────────────────────────────

def get_agent_or_redirect(request):
    """Helper: get the agent profile for the logged-in user."""
    try:
        return request.user.agent_profile
    except Agent.DoesNotExist:
        return None


@login_required(login_url='/login/')
def dashboard(request):
    """Agent dashboard — overview of their apartments."""
    agent = get_agent_or_redirect(request)
    if not agent:
        messages.error(request, "No agent profile found. Please contact support.")
        return redirect('apartments:home')

    apartments = agent.apartments.all()
    available = apartments.filter(status='available').count()
    booked = apartments.filter(status='booked').count()

    context = {
        'agent': agent,
        'apartments': apartments,
        'available': available,
        'booked': booked,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='/login/')
def add_apartment(request):
    """Add a new apartment listing."""
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('apartments:home')

    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.agent = agent
            apartment.save()
            form.save_m2m() # Save amenities

            # Handle gallery images
            files = request.FILES.getlist('gallery_images')
            for f in files:
                ApartmentImage.objects.create(apartment=apartment, image=f)

            messages.success(request, f'"{apartment.title}" has been listed!')
            return redirect('apartments:dashboard')
    else:
        form = ApartmentForm()

    return render(request, 'dashboard/apartment_form.html', {'form': form, 'action': 'Add'})


@login_required(login_url='/login/')
def edit_apartment(request, pk):
    """Edit an existing apartment."""
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('apartments:home')

    apartment = get_object_or_404(Apartment, pk=pk, agent=agent)

    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)
        if form.is_valid():
            apartment = form.save()
            
            # Handle gallery images
            files = request.FILES.getlist('gallery_images')
            for f in files:
                ApartmentImage.objects.create(apartment=apartment, image=f)
                
            messages.success(request, f'"{apartment.title}" has been updated!')
            return redirect('apartments:dashboard')
    else:
        form = ApartmentForm(instance=apartment)

    return render(request, 'dashboard/apartment_form.html', {'form': form, 'action': 'Edit', 'apartment': apartment})


@login_required(login_url='/login/')
def delete_apartment(request, pk):
    """Delete an apartment listing."""
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('apartments:home')

    apartment = get_object_or_404(Apartment, pk=pk, agent=agent)

    if request.method == 'POST':
        title = apartment.title
        apartment.delete()
        messages.success(request, f'"{title}" has been removed.')
        return redirect('apartments:dashboard')

    return render(request, 'dashboard/confirm_delete.html', {'apartment': apartment})


@login_required(login_url='/login/')
def edit_profile(request):
    """Edit agent profile."""
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('apartments:home')

    if request.method == 'POST':
        form = AgentProfileForm(request.POST, request.FILES, instance=agent)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('apartments:dashboard')
    else:
        form = AgentProfileForm(instance=agent)

    return render(request, 'dashboard/edit_profile.html', {'form': form})


@login_required(login_url='/login/')
def agent_bookings(request):
    """View all bookings for an agent's apartments."""
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('apartments:home')

    bookings = Booking.objects.filter(apartment__agent=agent).order_by('-created_at')
    
    context = {
        'agent': agent,
        'bookings': bookings,
    }
    return render(request, 'dashboard/bookings.html', context)


@login_required(login_url='/login/')
def update_booking_status(request, pk, status):
    """Update the status of a booking."""
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('apartments:home')

    booking = get_object_or_404(Booking, pk=pk, apartment__agent=agent)
    if status in ['confirmed', 'cancelled'] and booking.status != status:
        booking.status = status
        booking.save()
        messages.success(request, f"Booking status updated to {status.title()}.")
        
    return redirect('apartments:agent_bookings')
