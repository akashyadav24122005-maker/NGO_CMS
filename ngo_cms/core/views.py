from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import BlogPost, Project, Donation, Volunteer
from .forms import ContactForm, VolunteerForm


def home(request):
    projects = Project.objects.filter(is_active=True)[:3]
    blogs = BlogPost.objects.all()[:3]

    return render(request, "home.html", {
        "projects": projects,
        "blogs": blogs
    })


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
    return render(request, "projects.html", {
        "projects": all_projects
    })


def blog(request):
    posts = BlogPost.objects.all().order_by("-id")
    return render(request, "blog.html", {
        "posts": posts
    })


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("contact")

    return render(request, "contact.html", {
        "form": form
    })


def donate(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = request.POST.get("amount")

        Donation.objects.create(
            donor_name=name,
            email=email,
            amount=amount
        )

        messages.success(request, "Thank you for your donation!")
        return redirect("home")

    return render(request, "donate.html")


def volunteer(request):
    form = VolunteerForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Volunteer form submitted!")
            return redirect("volunteer")

    return render(request, "volunteer.html", {
        "form": form
    })


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

        messages.success(request, "Registration successful. Please login.")
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