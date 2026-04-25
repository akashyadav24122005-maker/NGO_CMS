from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("our-work/", views.our_work, name="our_work"),
    path("projects/", views.projects, name="projects"),
    path("media/", views.media, name="media"),
    path("get-involved/", views.get_involved, name="get_involved"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("volunteer/", views.volunteer, name="volunteer"),

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-page/", views.admin_only_page, name="admin_page"),

    path("donate/", views.donate, name="donate"),
    path("success/", views.success, name="success"),
    path("failed/", views.failed, name="failed"),
    path("cancelled/", views.cancelled, name="cancelled"),

    path("dashboard/banners/", views.banner_list, name="banner_list"),
    path(
        "dashboard/banner/delete/<int:pk>/",
        views.delete_banner,
        name="delete_banner"
    ),

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

    path('dashboard/vision/', views.vision_list, name='vision_list'),
    path('dashboard/vision/add/', views.vision_add, name='vision_add'),
    path('dashboard/vision/edit/<int:pk>/', views.vision_edit, name='vision_edit'),
    path('dashboard/vision/delete/<int:pk>/', views.vision_delete, name='vision_delete'),

    path('dashboard/statistics/', views.statistic_list, name='statistic_list'),
    path('dashboard/statistics/add/', views.statistic_add, name='statistic_add'),
    path('dashboard/statistics/edit/<int:pk>/', views.statistic_edit, name='statistic_edit'),
    path('dashboard/statistics/delete/<int:pk>/', views.statistic_delete, name='statistic_delete'),

    path('dashboard/initiatives/', views.initiative_list, name='initiative_list'),
    path('dashboard/projects/', views.project_list, name='project_list'),
     
    path('dashboard/blogs/', views.blog_admin_list, name='blog_admin_list'),
    path('dashboard/messages/', views.contact_list, name='contact_list'),
    path('dashboard/volunteers/', views.volunteer_list, name='volunteer_list'),
    path('dashboard/donations/', views.donation_list, name='donation_list'),

    path('about/', views.about, name='about'),
    path('dashboard/about/', views.manage_about, name='manage_about'),
    path('dashboard/about/core-value/delete/<int:pk>/', views.delete_core_value, name='delete_core_value'),
    path('dashboard/about/program/delete/<int:pk>/', views.delete_program, name='delete_program'),
    path('dashboard/about/team/delete/<int:pk>/', views.delete_team_member, name='delete_team_member'),

    path('dashboard/about/story/edit/<int:pk>/', views.edit_story, name='edit_story'),
    path('dashboard/about/core-value/edit/<int:pk>/', views.edit_core_value, name='edit_core_value'),
    path('dashboard/about/program/edit/<int:pk>/', views.edit_program, name='edit_program'),
    path('dashboard/about/team/edit/<int:pk>/', views.edit_team_member, name='edit_team_member'),


    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),

    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),

    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('dashboard/projects/', views.manage_projects, name='manage_projects'),
    path('dashboard/projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('dashboard/projects/delete/<int:pk>/', views.delete_project, name='delete_project'),

    path('media/', views.media, name='media'),
    path('dashboard/media/', views.manage_media, name='manage_media'),

    path('dashboard/media/press-release/edit/<int:pk>/', views.edit_press_release, name='edit_press_release'),
    path('dashboard/media/press-release/delete/<int:pk>/', views.delete_press_release, name='delete_press_release'),

    path('dashboard/media/coverage/edit/<int:pk>/', views.edit_media_coverage, name='edit_media_coverage'),
    path('dashboard/media/coverage/delete/<int:pk>/', views.delete_media_coverage, name='delete_media_coverage'),

    path('dashboard/media/gallery/edit/<int:pk>/', views.edit_gallery_image, name='edit_gallery_image'),
    path('dashboard/media/gallery/delete/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),

    path('dashboard/media/video/edit/<int:pk>/', views.edit_video, name='edit_video'),
    path('dashboard/media/video/delete/<int:pk>/', views.delete_video, name='delete_video'),

    path("dashboard/banners/add/", views.banner_add, name="banner_add"),
    path("dashboard/initiatives/add/", views.initiative_add, name="initiative_add"),
    path("dashboard/projects/add/", views.project_add, name="project_add"),
    path("dashboard/blogs/add/", views.blog_add, name="blog_add"),


]