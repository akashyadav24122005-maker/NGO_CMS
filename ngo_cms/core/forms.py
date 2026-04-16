from django import forms
from .models import ContactMessage, Donation, Volunteer


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'email', 'amount']


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['full_name', 'email', 'phone', 'interest']