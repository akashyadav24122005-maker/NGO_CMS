# core/urls.py  (Modified + Clean Final Version)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # -------------------------
    # Frontend Pages
    # -------------------------
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("our-work/", views.our_work, name="our_work"),
    path("projects/", views.projects, name="projects"),
    path("media/", views.media, name="media"),
    path("get-involved/", views.get_involved, name="get_involved"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("volunteer/", views.volunteer, name="volunteer"),

    # -------------------------
    # Authentication
    # -------------------------
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # -------------------------
    # Dashboard
    # -------------------------
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-page/", views.admin_only_page, name="admin_page"),

    # -------------------------
    # Donation + Razorpay
    # -------------------------
    path("donate/", views.donate, name="donate"),
    path("success/", views.success, name="success"),
    path("failed/", views.failed, name="failed"),
    path("cancelled/", views.cancelled, name="cancelled"),

    # -------------------------
    # Banner CRUD
    # -------------------------
    path("dashboard/banners/", views.banner_list, name="banner_list"),
    path(
        "dashboard/banner/delete/<int:pk>/",
        views.delete_banner,
        name="delete_banner"
    ),

    # -------------------------
    # Password Reset
    # -------------------------
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="forgot_password.html"
        ),
        name="password_reset"
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]