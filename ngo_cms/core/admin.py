# core/admin.py  (Modified + Clean Final Version)

from django.contrib import admin
from .models import (
    Banner,
    VisionMission,
    Statistic,
    Initiative,
    ContactMessage,
    Donation,
    Volunteer,
    BlogPost,
    Project,
)


# -------------------------
# Banner
# -------------------------
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "status")
    list_editable = ("order", "status")
    search_fields = ("title",)


# -------------------------
# Vision & Mission
# -------------------------
@admin.register(VisionMission)
class VisionMissionAdmin(admin.ModelAdmin):
    list_display = ("vision_title", "mission_title")


# -------------------------
# Statistics
# -------------------------
@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order", "status")
    list_editable = ("order", "status")


# -------------------------
# Initiatives
# -------------------------
@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "status")
    list_editable = ("order", "status")


# -------------------------
# Contact Messages
# -------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")


# -------------------------
# Donations
# -------------------------
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "donor_name",
        "email",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("donor_name", "email")


# -------------------------
# Volunteers
# -------------------------
@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "created_at",
    )
    search_fields = ("full_name", "email")


# -------------------------
# Blog Posts
# -------------------------
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)


# -------------------------
# Projects
# -------------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "location")