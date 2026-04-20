from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import BlogPost, Project, Donation, Volunteer
from .forms import ContactForm, VolunteerForm
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Donation
from django.shortcuts import render, redirect


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

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def donate(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        amount = int(request.POST['amount']) * 100

        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        donation = Donation.objects.create(
            donor_name=name,
            email=email,
            amount=amount // 100,
            order_id=razorpay_order['id'],
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
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            donation = Donation.objects.get(order_id=order_id)
            donation.payment_id = payment_id
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