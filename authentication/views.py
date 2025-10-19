
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        # Redirect to Members Portal dashboard
        return redirect('members_portal:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Set session expiry based on remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Browser close
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                # Always redirect to Members Portal after login
                return redirect('members_portal:dashboard')
            else:
                messages.error(request, 'Your account has been deactivated. Contact the administrator.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('authentication:login')


@csrf_protect
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email, is_active=True)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link (you'll need to implement the reset view)
            reset_link = f"{request.scheme}://{request.get_host()}/auth/reset/{uid}/{token}/"
            
            # Send email
            subject = 'Password Reset - Ruwe Holy Ghost Church'
            message = render_to_string('authentication/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
                'site_name': 'Ruwe Holy Ghost Church Management System'
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=message
            )
            
            messages.success(request, 'Password reset instructions have been sent to your email.')
            return redirect('authentication:login')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
    
    return render(request, 'authentication/forgot_password.html')


def get_user_context(request):
    """Helper function to get user context for templates"""
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            return {
                'user_display_name': request.user.first_name or request.user.username,
                'user_profile_picture': profile.get_profile_picture,
                'user_position': profile.position
            }
        except:
            return {
                'user_display_name': request.user.username,
                'user_profile_picture': 'https://i.imgur.com/UkrjXEc.jpg',
                'user_position': 'Church Administrator'
            }
    return {}
