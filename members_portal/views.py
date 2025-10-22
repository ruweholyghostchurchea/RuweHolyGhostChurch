
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
        'home_church_head_teacher': home_church_head_teacher,
        'home_church_assistant_teachers': home_church_assistant_teachers,
        'home_church_members': home_church_members,
        'town_church_members': town_church_members,
    }
    
    return render(request, 'members_portal/my_church.html', context)


@login_required
def my_pastorate(request):
    """
    Member's pastorate view - shows detailed information about member's pastorate
    """
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        return render(request, 'members_portal/no_profile.html', {
            'user': request.user
        })
    
    # Get Pastorate
    pastorate = member.user_home_pastorate
    
    if not pastorate:
        context = {
            'member': member,
            'is_admin': request.user.is_staff or request.user.is_superuser,
            'pastorate': None,
        }
        return render(request, 'members_portal/my_pastorate.html', context)
    
    # Get Pastor (member with pastorate_pastor role in this pastorate)
    pastor = None
    try:
        pastor = Member.objects.filter(
            church_clergy_roles__contains=['pastorate_pastor'],
            user_home_pastorate=pastorate,
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Pastor's Wife (if pastor exists)
    pastor_wife = None
    if pastor and pastor.marital_status == 'married':
        try:
            pastor_wife = Member.objects.filter(
                church_clergy_roles__contains=['pastorate_pastor_wife'],
                user_home_pastorate=pastorate,
                membership_status='Active',
                last_name=pastor.last_name
            ).first()
        except:
            pass
    
    # Get Pastorate leaders
    woman_leader = Member.objects.filter(
        church_clergy_roles__contains=['pastorate_woman_leader'],
        user_home_pastorate=pastorate,
        membership_status='Active'
    ).first()
    
    woman_leader_husband = None
    if woman_leader and woman_leader.marital_status == 'married':
        woman_leader_husband = Member.objects.filter(
            church_clergy_roles__contains=['pastorate_woman_leader_husband'],
            user_home_pastorate=pastorate,
            membership_status='Active',
            last_name=woman_leader.last_name
        ).first()
    
    division = Member.objects.filter(
        church_clergy_roles__contains=['pastorate_division'],
        user_home_pastorate=pastorate,
        membership_status='Active'
    ).first()
    
    division_wife = None
    division_husband = None
    if division:
        if division.gender == 'M' and division.marital_status == 'married':
            division_wife = Member.objects.filter(
                church_clergy_roles__contains=['pastorate_division_wife'],
                user_home_pastorate=pastorate,
                membership_status='Active',
                last_name=division.last_name
            ).first()
        elif division.gender == 'F' and division.marital_status == 'married':
            division_husband = Member.objects.filter(
                church_clergy_roles__contains=['pastorate_division_husband'],
                user_home_pastorate=pastorate,
                membership_status='Active',
                last_name=division.last_name
            ).first()
    
    lay_reader = Member.objects.filter(
        church_clergy_roles__contains=['pastorate_lay_reader'],
        user_home_pastorate=pastorate,
        membership_status='Active'
    ).first()
    
    lay_reader_wife = None
    if lay_reader and lay_reader.marital_status == 'married':
        lay_reader_wife = Member.objects.filter(
            church_clergy_roles__contains=['pastorate_lay_reader_wife'],
            user_home_pastorate=pastorate,
            membership_status='Active',
            last_name=lay_reader.last_name
        ).first()
    
    # Get Mission Church for this pastorate
    from church_structure.models import Church
    mission_church = None
    try:
        mission_church = Church.objects.filter(
            pastorate=pastorate,
            is_mission_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    # Get all churches in this pastorate
    churches = Church.objects.filter(
        pastorate=pastorate,
        is_active=True
    ).order_by('name')
    
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
        'pastorate': pastorate,
        'pastor': pastor,
        'pastor_wife': pastor_wife,
        'woman_leader': woman_leader,
        'woman_leader_husband': woman_leader_husband,
        'division': division,
        'division_wife': division_wife,
        'division_husband': division_husband,
        'lay_reader': lay_reader,
        'lay_reader_wife': lay_reader_wife,
        'mission_church': mission_church,
        'churches': churches,
    }
    
    return render(request, 'members_portal/my_pastorate.html', context)


@login_required
def my_diocese(request):
    """
    Member's diocese view - shows detailed information about member's diocese
    """
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        return render(request, 'members_portal/no_profile.html', {
            'user': request.user
        })
    
    # Get Diocese
    diocese = member.user_home_diocese
    
    if not diocese:
        context = {
            'member': member,
            'is_admin': request.user.is_staff or request.user.is_superuser,
            'diocese': None,
        }
        return render(request, 'members_portal/my_diocese.html', context)
    
    # Get Bishop (member with diocese_bishop role in this diocese)
    bishop = None
    try:
        bishop = Member.objects.filter(
            church_clergy_roles__contains=['diocese_bishop'],
            user_home_diocese=diocese,
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Bishop's Wife (if bishop exists)
    bishop_wife = None
    if bishop and bishop.marital_status == 'married':
        try:
            bishop_wife = Member.objects.filter(
                church_clergy_roles__contains=['diocese_bishop_wife'],
                user_home_diocese=diocese,
                membership_status='Active',
                last_name=bishop.last_name
            ).first()
        except:
            pass
    
    # Get Diocesan Church for this diocese
    from church_structure.models import Church
    diocesan_church = None
    try:
        diocesan_church = Church.objects.filter(
            pastorate__diocese=diocese,
            is_diocesan_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    # Get all pastorates in this diocese
    from church_structure.models import Pastorate
    pastorates = Pastorate.objects.filter(
        diocese=diocese,
        is_active=True
    ).order_by('name')
    
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
        'diocese': diocese,
        'bishop': bishop,
        'bishop_wife': bishop_wife,
        'diocesan_church': diocesan_church,
        'pastorates': pastorates,
    }
    
    return render(request, 'members_portal/my_diocese.html', context)


@login_required
def my_headquarters(request):
    """
    Member's headquarters view - shows Archbishop, Headquarters Church, King, and King's Pillar information
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
    
    # Get King's Pillar (member with dean_kings_pillar role)
    kings_pillar = None
    try:
        kings_pillar = Member.objects.filter(
            special_clergy_roles__contains=['dean_kings_pillar'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    context = {
        'member': member,
        'is_admin': request.user.is_staff or request.user.is_superuser,
        'archbishop': archbishop,
        'king': king,
        'headquarter_church': headquarter_church,
        'kings_pillar': kings_pillar,
    }
    
    return render(request, 'members_portal/my_headquarters.html', context)


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
