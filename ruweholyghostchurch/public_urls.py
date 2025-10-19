"""
Public Website URL Configuration for ruweholyghostchurch.org
Public-facing website (no login required)
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Authentication URLs (for member login from public site)
    path('auth/', include('authentication.urls')),

    # Public website URLs
    path('', include('public_site.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)