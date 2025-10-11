"""
Members Portal URL Configuration for members.ruweholyghostchurch.org
Member-facing portal (login required)
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import member portal views (to be created)
# from members_portal import views

urlpatterns = [
    # Member authentication (separate from admin)
    path('auth/', include('authentication.urls')),  # Reuse auth for member login
    
    # Member portal URLs will be added here
    # path('', views.dashboard, name='member_dashboard'),
    # path('profile/', views.profile, name='member_profile'),
    # path('attendance/', views.attendance, name='member_attendance'),
    # path('giving/', views.giving, name='member_giving'),
    
    # Placeholder for now - redirects to login
    path('', lambda request: __import__('django.shortcuts').shortcuts.redirect('authentication:login')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
