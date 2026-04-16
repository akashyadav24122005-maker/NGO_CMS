from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('our-work/', views.our_work, name='our_work'),
    path('projects/', views.projects, name='projects'),
    path('media/', views.media, name='media'),
    path('get-involved/', views.get_involved, name='get_involved'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-page/', views.admin_only_page, name='admin_page'),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='forgot_password.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]