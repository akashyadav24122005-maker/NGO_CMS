# core/views.py  (Modified + Clean Final Version)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

import razorpay

from .models import (
    Banner,
    VisionMission,
    Statistic,
    Initiative,
    Donation,
    Volunteer,
    BlogPost,
    Project,
    ContactMessage,
)
from .forms import ContactForm, VolunteerForm


# -------------------------
# Razorpay Client
# -------------------------
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


# -------------------------
# Frontend Pages
# -------------------------
def home(request):
    banners = Banner.objects.filter(status=True).order_by("order")
    vm = VisionMission.objects.first()
    stats = Statistic.objects.filter(status=True).order_by("order")
    initiatives = Initiative.objects.filter(status=True).order_by("order")

    projects = Project.objects.filter(is_active=True)[:3]
    blogs = BlogPost.objects.all().order_by("-id")[:3]

    context = {
        "banners": banners,
        "vm": vm,
        "stats": stats,
        "initiatives": initiatives,
        "projects": projects,
        "blogs": blogs,
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


def our_work(request):
    return render(request, "our_work.html")


def media(request):
    return render(request, "media.html")


def get_involved(request):
    return render(request, "get_involved.html")


def projects(request):
    all_projects = Project.objects.all()
    return render(request, "projects.html", {"projects": all_projects})


def blog(request):
    posts = BlogPost.objects.all().order_by("-id")
    return render(request, "blog.html", {"posts": posts})


# -------------------------
# Contact
# -------------------------
def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("contact")

    return render(request, "contact.html", {"form": form})


# -------------------------
# Donation + Razorpay
# -------------------------
def donate(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = int(request.POST.get("amount"))

        razorpay_order = client.order.create({
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": "1"
        })

        Donation.objects.create(
            donor_name=name,
            email=email,
            amount=amount,
            order_id=razorpay_order["id"],
            status="Pending"
        )

        return render(request, "payment.html", {
            "payment": razorpay_order,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    return render(request, "donate.html")


def success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            donation = Donation.objects.get(order_id=order_id)
            donation.payment_id = payment_id
            donation.signature = signature
            donation.status = "Success"
            donation.save()

            return render(request, "success.html")

        except:
            donation = Donation.objects.get(order_id=order_id)
            donation.status = "Failed"
            donation.save()

            return redirect("failed")


def failed(request):
    return render(request, "failed.html")


def cancelled(request):
    order_id = request.GET.get("order_id")

    if order_id:
        try:
            donation = Donation.objects.get(order_id=order_id)
            donation.status = "Cancelled"
            donation.save()
        except:
            pass

    return render(request, "cancelled.html")


# -------------------------
# Volunteer
# -------------------------
def volunteer(request):
    form = VolunteerForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Volunteer form submitted!")
            return redirect("volunteer")

    return render(request, "volunteer.html", {"form": form})


# -------------------------
# Authentication
# -------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")

        messages.error(request, "Invalid username or password!")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


# -------------------------
# Dashboard
# -------------------------
@login_required
def dashboard(request):
    context = {
        "total_blogs": BlogPost.objects.count(),
        "total_projects": Project.objects.count(),
        "total_donations": Donation.objects.count(),
        "total_volunteers": Volunteer.objects.count(),
    }
    return render(request, "dashboard.html", context)


@staff_member_required
def admin_only_page(request):
    return render(request, "admin_page.html")


# -------------------------
# Banner CRUD Example
# -------------------------
def banner_list(request):
    banners = Banner.objects.all().order_by("order")
    return render(request, "dashboard/banner_list.html", {"banners": banners})


def delete_banner(request, pk):
    banner = get_object_or_404(Banner, id=pk)
    banner.delete()
    messages.success(request, "Banner deleted successfully!")
    return redirect("banner_list")