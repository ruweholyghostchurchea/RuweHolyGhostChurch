
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from members.models import Member


@login_required
def dashboard(request):
    """
    Member dashboard - shows member's personal information and overview
    
    This view displays comprehensive member information organized in cards:
    - Personal details (name, baptismal name, username, identifier)
    - Contact information (phone, email, location)
    - Church hierarchy (home and town church assignments)
    - Membership status and roles
    - Emergency contacts
    - Family relationships
    - Job/occupation details
    - Documents and profile photo
    
    If the user is a staff member (admin), they get a link to the CMS dashboard.
    """
    try:
        # Get the member profile linked to the logged-in user
        member = request.user.member_profile
    except Member.DoesNotExist:
        # If no member profile exists, show error message
        return render(request, 'members_portal/no_profile.html', {
            'user': request.user
        })
    
    # Prepare context data for the template
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
        # Additional computed fields for display
        'age': _calculate_age(member.date_of_birth) if member.date_of_birth else None,
        'membership_duration': _calculate_membership_duration(member.date_joined_religion) if member.date_joined_religion else None,
    }
    
    return render(request, 'members_portal/dashboard.html', context)


@login_required
def profile(request):
    """
    Member profile view - allows member to view their detailed information
    This is a read-only view; editing is done through the admin CMS.
    """
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        return render(request, 'members_portal/no_profile.html', {
            'user': request.user
        })
    
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'members_portal/profile.html', context)


@login_required
def attendance(request):
    """
    Member attendance history view
    Shows the member's attendance records across all church services.
    """
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        return render(request, 'members_portal/no_profile.html', {
            'user': request.user
        })
    
    # TODO: Implement attendance filtering and display
    # For now, just render the template
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'members_portal/attendance.html', context)


@login_required
def giving(request):
    """
    Member giving/contribution history view
    Shows the member's financial contributions and tithe records.
    """
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        return render(request, 'members_portal/no_profile.html', {
            'user': request.user
        })
    
    # TODO: Implement giving/contribution filtering and display
    # For now, just render the template
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    
    return render(request, 'members_portal/giving.html', context)


# Helper functions for calculations
def _calculate_age(date_of_birth):
    """Calculate age from date of birth"""
    from datetime import date
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age


def _calculate_membership_duration(date_joined):
    """Calculate membership duration in years and months"""
    from datetime import date
    today = date.today()
    years = today.year - date_joined.year
    months = today.month - date_joined.month
    
    if months < 0:
        years -= 1
        months += 12
    
    return {'years': years, 'months': months}
