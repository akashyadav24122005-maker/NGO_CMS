from django import forms
from .models import (
    ContactMessage,
    Donation,
    Volunteer,
    Banner,
    VisionMission,
    Statistic,
    Initiative,
    Project,
    BlogPost,
)

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your Message'
            }),
        }


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'email', 'amount']
        widgets = {
            'donor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Donation Amount'
            }),
        }


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['full_name', 'email', 'phone', 'interest']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'interest': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area of Interest'
            }),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'


class VisionMissionForm(forms.ModelForm):
    class Meta:
        model = VisionMission
        fields = '__all__'


class StatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = '__all__'


class InitiativeForm(forms.ModelForm):
    class Meta:
        model = Initiative
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = '__all__'