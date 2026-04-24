# core/models.py  (Fixed Clean Final Version)

from django.db import models
from django.utils import timezone


# -------------------------
# Banner Slider
# -------------------------
class Banner(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="banners/")
    order = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# -------------------------
# Vision & Mission
# -------------------------
class VisionMission(models.Model):
    vision_title = models.CharField(max_length=150)
    vision_description = models.TextField()
    mission_title = models.CharField(max_length=150)
    mission_description = models.TextField()

    def __str__(self):
        return "Vision & Mission"


# -------------------------
# Statistics
# -------------------------
class Statistic(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.label


# -------------------------
# Initiatives
# -------------------------
class Initiative(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="initiatives/")
    order = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# -------------------------
# Contact Messages
# -------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------------
# Donations
# -------------------------
class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=200, blank=True, null=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    signature = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending",   "Pending"),
            ("Success",   "Success"),
            ("Failed",    "Failed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - ₹{self.amount}"


# -------------------------
# Volunteers
# -------------------------
class Volunteer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interest = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# -------------------------
# Blog Posts
# -------------------------
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# -------------------------
# Our Story
# -------------------------
class OurStory(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Our Story"


# -------------------------
# Core Values
# -------------------------
class CoreValue(models.Model):
    value = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value


# -------------------------
# Programs
# -------------------------
class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------------
# Team Members
# -------------------------
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------------
# Our Impact
# -------------------------
class OurImpact(models.Model):
    achievement = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'our_impact'

    def __str__(self):
        return self.achievement


from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ongoing')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# Add this NEW model below Project
class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='project_images/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'project_images'

    def __str__(self):
        return f"Image for {self.project.title}"
