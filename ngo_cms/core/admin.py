from django.contrib import admin
from .models import ContactMessage, Project, Volunteer, Donation, BlogPost

admin.site.register(ContactMessage)
admin.site.register(Donation)
admin.site.register(Project)
admin.site.register(Volunteer)
admin.site.register(BlogPost)

