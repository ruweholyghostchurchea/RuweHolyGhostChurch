"""
Members Portal URL Configuration for members.ruweholyghostchurch.org
Member-facing portal (login required)
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Member authentication (separate from admin)
    path('auth/', include('authentication.urls')),  # Reuse auth for member login
    
    # Member portal URLs
    path('', include('members_portal.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
