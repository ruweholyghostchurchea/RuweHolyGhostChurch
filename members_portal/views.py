
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
def my_church(request):
    """
    Member's church view - shows detailed information about member's home and town church
    """
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        return render(request, 'members_portal/no_profile.html', {
            'user': request.user
        })
    
    # Get Archbishop (member with dean_archbishop role)
    archbishop = None
    try:
        archbishop = Member.objects.filter(
            church_clergy_roles__contains=['dean_archbishop'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get King (member with dean_king role)
    king = None
    try:
        king = Member.objects.filter(
            special_clergy_roles__contains=['dean_king'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Headquarter Church
    from church_structure.models import Church
    headquarter_church = None
    try:
        headquarter_church = Church.objects.filter(
            is_headquarter_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    # Get home church teachers
    home_church_head_teacher = None
    home_church_assistant_teachers = []
    if member.user_home_church:
        home_church_head_teacher = member.user_home_church.head_teacher
        home_church_assistant_teachers = list(member.user_home_church.teachers.filter(membership_status='Active'))
    
    # Get home church members
    home_church_members = []
    if member.user_home_church:
        home_church_members = Member.objects.filter(
            user_home_church=member.user_home_church,
            membership_status='Active'
        ).order_by('first_name', 'last_name')
    
    # Get town church members (if applicable)
    town_church_members = []
    if member.user_town_church:
        town_church_members = Member.objects.filter(
            user_home_church=member.user_town_church,
            membership_status='Active'
        ).order_by('first_name', 'last_name')
    
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
        'archbishop': archbishop,
        'king': king,
        'headquarter_church': headquarter_church,
        'home_church_head_teacher': home_church_head_teacher,
        'home_church_assistant_teachers': home_church_assistant_teachers,
        'home_church_members': home_church_members,
        'town_church_members': town_church_members,
    }
    
    return render(request, 'members_portal/my_church.html', context)


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
