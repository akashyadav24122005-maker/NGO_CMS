# ngo_cms/urls.py  (Modified + Clean Final Version)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin Panel
    path("admin/", admin.site.urls),

    # App URLs
    path("", include("core.urls")),
]


# -------------------------
# Media Files in Development
# -------------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )