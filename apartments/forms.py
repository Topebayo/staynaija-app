from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Agent, Apartment, Booking, Amenity, ApartmentImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class AgentSignupForm(UserCreationForm):
    """Registration form for new agents."""
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
        'placeholder': 'Full name',
        'class': 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm',
    }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': '+234 801 234 5678',
        'class': 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'you@example.com',
        'class': 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style the default User fields
        input_class = 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm'
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username', 'class': input_class})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password', 'class': input_class})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password', 'class': input_class})
        # Remove help texts for cleaner UI
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Agent.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
            )
        return user


class LoginForm(forms.Form):
    """Simple login form."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm',
    }))


class ApartmentForm(forms.ModelForm):
    """Form for agents to add/edit apartments."""
    class Meta:
        model = Apartment
        fields = ('title', 'description', 'location', 'price', 'bedrooms', 'bathrooms', 'status', 'amenities', 'image')

    gallery_images = MultipleFileField(required=False, help_text="Upload additional images for the gallery")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_class = 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm'
        textarea_class = input_class + ' resize-none'
        select_class = input_class

        self.fields['title'].widget.attrs.update({'placeholder': 'e.g. Luxury 3-Bedroom Apartment', 'class': input_class})
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder': 'Describe the apartment...', 'class': textarea_class, 'rows': 4})
        self.fields['location'].widget.attrs.update({'placeholder': 'e.g. Victoria Island, Lagos', 'class': input_class})
        self.fields['price'].widget.attrs.update({'placeholder': 'Price per night in Naira', 'class': input_class})
        self.fields['bedrooms'].widget.attrs.update({'class': select_class, 'min': 1})
        self.fields['bathrooms'].widget.attrs.update({'class': select_class, 'min': 1})
        self.fields['status'].widget.attrs.update({'class': select_class})
        
        checkbox_class = 'w-4 h-4 text-gold-600 bg-gray-100 dark:bg-rich-900 border-gray-300 dark:border-rich-800 rounded-none focus:ring-gold-500'
        self.fields['amenities'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'})
        
        file_input_class = 'w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-none file:border-0 file:text-sm file:font-semibold file:bg-gray-100 dark:file:bg-rich-950 file:text-rich-900 dark:file:text-white hover:file:bg-gray-200 dark:hover:file:bg-rich-800 cursor-pointer'
        self.fields['image'].widget.attrs.update({'class': file_input_class})
        self.fields['gallery_images'].widget.attrs.update({'class': file_input_class})


class AgentProfileForm(forms.ModelForm):
    """Form for agents to edit their profile."""
    class Meta:
        model = Agent
        fields = ('name', 'phone', 'email', 'bio', 'photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_class = 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm'
        self.fields['name'].widget.attrs.update({'class': input_class})
        self.fields['phone'].widget.attrs.update({'class': input_class})
        self.fields['email'].widget.attrs.update({'class': input_class})
        self.fields['bio'].widget = forms.Textarea(attrs={'class': input_class + ' resize-none', 'rows': 3, 'placeholder': 'Tell guests about yourself...'})
        self.fields['photo'].widget.attrs.update({'class': 'w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-none file:border-0 file:text-sm file:font-semibold file:bg-gray-100 dark:file:bg-rich-950 file:text-rich-900 dark:file:text-white hover:file:bg-gray-200 dark:hover:file:bg-rich-800 cursor-pointer'})


class BookingForm(forms.ModelForm):
    """Form for guests to book an apartment."""
    class Meta:
        model = Booking
        fields = ('guest_name', 'guest_email', 'guest_phone', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_class = 'w-full px-4 py-3 rounded-none border border-gray-200 dark:border-rich-800 dark:bg-rich-900 dark:text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 outline-none transition text-sm'
        
        self.fields['guest_name'].widget.attrs.update({'placeholder': 'Full Name', 'class': input_class})
        self.fields['guest_email'].widget.attrs.update({'placeholder': 'Email Address', 'class': input_class})
        self.fields['guest_phone'].widget.attrs.update({'placeholder': 'Phone Number', 'class': input_class})
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': input_class})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': input_class})
