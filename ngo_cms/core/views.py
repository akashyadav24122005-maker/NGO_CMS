from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.shortcuts import render
from .models import OurStory, CoreValue, Program, TeamMember

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import (
    VisionMissionForm, StatisticForm, InitiativeForm,
    ProjectForm, BlogPostForm
)
from .models import (
    VisionMission, Statistic, Initiative,
    Project, BlogPost, ContactMessage
)


client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


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


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("contact")

    return render(request, "contact.html", {"form": form})

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

def volunteer(request):
    form = VolunteerForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Volunteer form submitted!")
            return redirect("volunteer")

    return render(request, "volunteer.html", {"form": form})

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

@login_required
def dashboard(request):
    context = {
        "total_blogs": BlogPost.objects.count(),
        "total_projects": Project.objects.count(),
        "total_donations": Donation.objects.count(),
        "total_volunteers": Volunteer.objects.count(),
    }
    # FROM:
    return render(request, "dashboard.html", context)
    # TO: (no change needed here since dashboard.html is in templates/)
    return render(request, "dashboard.html", context)


@staff_member_required
def admin_only_page(request):
    return render(request, "admin_page.html")

def banner_list(request):
    banners = Banner.objects.all().order_by("order")
    return render(request, "dashboard/banner_list.html", {"banners": banners})


def delete_banner(request, pk):
    banner = get_object_or_404(Banner, id=pk)
    banner.delete()
    messages.success(request, "Banner deleted successfully!")
    return redirect("banner_list")


@login_required
def vision_list(request):
    data = VisionMission.objects.all()
    return render(request, 'dashboard/vision_list.html', {'data': data})

@login_required
def vision_add(request):
    form = VisionMissionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vision_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Add Vision'})

@login_required
def vision_edit(request, pk):
    obj = get_object_or_404(VisionMission, pk=pk)
    form = VisionMissionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('vision_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Edit Vision'})

@login_required
def vision_delete(request, pk):
    get_object_or_404(VisionMission, pk=pk).delete()
    return redirect('vision_list')

@login_required
def statistic_list(request):
    data = Statistic.objects.all()
    return render(request, 'dashboard/statistic_list.html', {'data': data})

@login_required
def statistic_add(request):
    form = StatisticForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('statistic_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Add Statistic'})

@login_required
def statistic_edit(request, pk):
    obj = get_object_or_404(Statistic, pk=pk)
    form = StatisticForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('statistic_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Edit Statistic'})

@login_required
def statistic_delete(request, pk):
    get_object_or_404(Statistic, pk=pk).delete()
    return redirect('statistic_list')


# Initiative CRUD
@login_required
def initiative_list(request):
    data = Initiative.objects.all()
    return render(request, 'dashboard/initiative_list.html', {'data': data})

@login_required
def initiative_add(request):
    form = InitiativeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('initiative_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Add Initiative'})

@login_required
def initiative_edit(request, pk):
    obj = get_object_or_404(Initiative, pk=pk)
    form = InitiativeForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('initiative_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Edit Initiative'})

@login_required
def initiative_delete(request, pk):
    get_object_or_404(Initiative, pk=pk).delete()
    return redirect('initiative_list')

# Project CRUD
@login_required
def project_list(request):
    data = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'data': data})

@login_required
def project_add(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('project_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Add Project'})

@login_required
def project_edit(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('project_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Edit Project'})

@login_required
def project_delete(request, pk):
    get_object_or_404(Project, pk=pk).delete()
    return redirect('project_list')


# Blog CRUD
@login_required
def blog_admin_list(request):
    data = BlogPost.objects.all()
    return render(request, 'dashboard/blog_list.html', {'data': data})

@login_required
def blog_add(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('blog_admin_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Add Blog'})

@login_required
def blog_edit(request, pk):
    obj = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('blog_admin_list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Edit Blog'})

@login_required
def blog_delete(request, pk):
    get_object_or_404(BlogPost, pk=pk).delete()
    return redirect('blog_admin_list')

# Contact Messages
@login_required
def contact_list(request):
    data = ContactMessage.objects.all().order_by('-id')
    return render(request, 'dashboard/contact_list.html', {'data': data})

@login_required
def contact_delete(request, pk):
    get_object_or_404(ContactMessage, pk=pk).delete()
    return redirect('contact_list')


@login_required
def volunteer_list(request):
    data = Volunteer.objects.all().order_by('-created_at')
    return render(request, 'dashboard/volunteer_list.html', {'data': data})

@login_required
def donation_list(request):
    data = Donation.objects.all().order_by('-created_at')
    return render(request, 'dashboard/donation_list.html', {'data': data})




from .models import OurStory, CoreValue, Program, TeamMember
from .forms import OurStoryForm, CoreValueForm, ProgramForm, TeamMemberForm

# ── PUBLIC ABOUT PAGE ─────────────────────────────────
def about(request):
    story = OurStory.objects.first()
    core_values = CoreValue.objects.all()
    programs = Program.objects.all()
    team = TeamMember.objects.all()
    vision_mission = VisionMission.objects.first()
    return render(request, 'about.html', {
        'story': story,
        'core_values': core_values,
        'programs': programs,
        'team': team,
        'vision_mission': vision_mission,
    })


# ── ABOUT US DASHBOARD ────────────────────────────────
@login_required
def manage_about(request):
    story = OurStory.objects.first()
    story_form = OurStoryForm(instance=story)
    cv_form = CoreValueForm()
    prog_form = ProgramForm()
    team_form = TeamMemberForm()

    if request.method == 'POST':
        section = request.POST.get('section')

        if section == 'story':
            story_form = OurStoryForm(request.POST, instance=story)
            if story_form.is_valid():
                story_form.save()
                messages.success(request, 'Story updated!')
                return redirect('manage_about')

        elif section == 'core_value':
            cv_form = CoreValueForm(request.POST)
            if cv_form.is_valid():
                cv_form.save()
                messages.success(request, 'Core value added!')
                return redirect('manage_about')

        elif section == 'program':
            prog_form = ProgramForm(request.POST)
            if prog_form.is_valid():
                prog_form.save()
                messages.success(request, 'Program added!')
                return redirect('manage_about')

        elif section == 'team':
            team_form = TeamMemberForm(request.POST, request.FILES)
            if team_form.is_valid():
                team_form.save()
                messages.success(request, 'Team member added!')
                return redirect('manage_about')

    return render(request, 'dashboard/about_manage.html', {
        'story': story,
        'story_form': story_form,
        'core_values': CoreValue.objects.all(),
        'cv_form': cv_form,
        'programs': Program.objects.all(),
        'prog_form': prog_form,
        'team': TeamMember.objects.all(),
        'team_form': team_form,
    })


# ── DELETE VIEWS ──────────────────────────────────────
@login_required
def delete_core_value(request, pk):
    get_object_or_404(CoreValue, pk=pk).delete()
    messages.success(request, 'Deleted!')
    return redirect('manage_about')

@login_required
def delete_program(request, pk):
    get_object_or_404(Program, pk=pk).delete()
    messages.success(request, 'Deleted!')
    return redirect('manage_about')

@login_required
def delete_team_member(request, pk):
    get_object_or_404(TeamMember, pk=pk).delete()
    messages.success(request, 'Deleted!')
    return redirect('manage_about')


# ── EDIT VIEWS FOR ABOUT US ───────────────────────────

@login_required
def edit_story(request, pk):
    story = get_object_or_404(OurStory, pk=pk)
    form = OurStoryForm(request.POST or None, instance=story)
    if form.is_valid():
        form.save()
        messages.success(request, 'Story updated!')
        return redirect('manage_about')
    return render(request, 'dashboard/about_edit_form.html', {
        'form': form, 'title': 'Edit Our Story'
    })


@login_required
def edit_core_value(request, pk):
    obj = get_object_or_404(CoreValue, pk=pk)
    form = CoreValueForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Core value updated!')
        return redirect('manage_about')
    return render(request, 'dashboard/about_edit_form.html', {
        'form': form, 'title': 'Edit Core Value'
    })


@login_required
def edit_program(request, pk):
    obj = get_object_or_404(Program, pk=pk)
    form = ProgramForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Program updated!')
        return redirect('manage_about')
    return render(request, 'dashboard/about_edit_form.html', {
        'form': form, 'title': 'Edit Program'
    })


@login_required
def edit_team_member(request, pk):
    obj = get_object_or_404(TeamMember, pk=pk)
    form = TeamMemberForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Team member updated!')
        return redirect('manage_about')
    return render(request, 'dashboard/about_edit_form.html', {
        'form': form, 'title': 'Edit Team Member'
    })


# ── BLOG PUBLIC PAGES ─────────────────────────────────

def blog_list(request):
    blogs = BlogPost.objects.filter(status=True).order_by('-created_at')
    return render(request, 'blog.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, status=True)
    recent = BlogPost.objects.filter(status=True).exclude(pk=pk)[:3]
    return render(request, 'blog_detail.html', {'blog': blog, 'recent': recent})



from .models import Project, ProjectImage

def projects_list(request):
    status_filter = request.GET.get('status', '')
    if status_filter in ['Ongoing', 'Completed', 'Upcoming']:
        projects = Project.objects.filter(
            is_active=True, status=status_filter
        )
    else:
        projects = Project.objects.filter(is_active=True)

    # Impact stats
    total_projects = Project.objects.filter(is_active=True).count()
    ongoing = Project.objects.filter(status='Ongoing').count()
    completed = Project.objects.filter(status='Completed').count()

    return render(request, 'projects.html', {
        'projects': projects,
        'status_filter': status_filter,
        'total_projects': total_projects,
        'ongoing': ongoing,
        'completed': completed,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, is_active=True)
    images = project.images.all()
    related = Project.objects.filter(
        is_active=True
    ).exclude(pk=pk)[:3]
    return render(request, 'project_detail.html', {
        'project': project,
        'images': images,
        'related': related,
    })


# ── ADMIN PROJECT MANAGEMENT ──────────────────────────
@login_required
def manage_projects(request):
    projects = Project.objects.all().order_by('-created_at')
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            # Handle multiple image uploads
            for img in request.FILES.getlist('extra_images'):
                ProjectImage.objects.create(project=project, image=img)
            messages.success(request, 'Project saved successfully!')
            return redirect('manage_projects')

    return render(request, 'dashboard/project_manage.html', {
        'projects': projects,
        'form': form,
    })


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('manage_projects')

    return render(request, 'dashboard/project_edit.html', {
        'form': form,
        'project': project,
    })


@login_required
def delete_project(request, pk):
    get_object_or_404(Project, pk=pk).delete()
    messages.success(request, 'Project deleted!')
    return redirect('manage_projects')
