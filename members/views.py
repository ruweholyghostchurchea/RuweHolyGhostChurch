from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Member, MemberDocument
from church_structure.models import Diocese, Pastorate, Church
import json

@login_required
def index(request):
    """Members main view with search and pagination"""
    search_query = request.GET.get('search', '')
    user_group_filter = request.GET.get('user_group', '')
    diocese_filter = request.GET.get('diocese', '')

    members = Member.objects.exclude(membership_status__in=['Left/Quit', 'Dead']).select_related(
        'user_home_diocese', 'user_home_pastorate', 'user_home_church',
        'user_town_diocese', 'user_town_pastorate', 'user_town_church',
        'father', 'mother', 'guardian', 'brother', 'sister', 'uncle', 'aunt', 'friend'
    )

    # Apply filters
    if search_query:
        members = members.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if user_group_filter:
        members = members.filter(user_group=user_group_filter)

    if diocese_filter:
        members = members.filter(user_home_diocese_id=diocese_filter)

    # Pagination
    paginator = Paginator(members, 20)  # 20 members per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get data for filters
    dioceses = Diocese.objects.filter(is_active=True).order_by('country', 'name')
    user_groups = Member.USER_GROUP_CHOICES

    # Statistics
    active_members = Member.objects.filter(membership_status='Active')
    stats = {
        'total_members': active_members.count(),
        'youth_count': active_members.filter(user_group='Youth').count(),
        'adult_count': active_members.filter(user_group='Adult').count(),
        'elder_count': active_members.filter(user_group='Elder').count(),
        'clergy_count': active_members.filter(user_group='Clergy').count(),
        'staff_count': active_members.filter(is_staff=True).count(),
        'ordained_count': active_members.filter(is_ordained=True).count(),
        'pwd_count': active_members.filter(is_pwd=True).count(),
    }

    context = {
        'page_title': 'Members Management',
        'members': page_obj,
        'dioceses': dioceses,
        'user_groups': user_groups,
        'stats': stats,
        'search_query': search_query,
        'user_group_filter': user_group_filter,
        'diocese_filter': diocese_filter,
    }
    return render(request, 'members/index.html', context)

@login_required
def add_member(request):
    """Add new member view"""
    if request.method == 'GET':
        dioceses = Diocese.objects.filter(is_active=True).order_by('country', 'name')
        context = {
            'page_title': 'Add New Member',
            'dioceses': dioceses,
            'membership_statuses': Member.MEMBERSHIP_STATUS_CHOICES,
            'pwd_types': Member.PWD_TYPE_CHOICES,
            'member_roles': Member.MEMBER_ROLES,
            'church_clergy_roles': Member.CHURCH_CLERGY_ROLES,
            'special_clergy_roles': Member.SPECIAL_CLERGY_ROLES,
            'job_categories': Member.JOB_CATEGORIES,
            'job_choices': Member.JOB_CHOICES,
        }
        return render(request, 'members/add_member.html', context)

    elif request.method == 'POST':
        try:
            # Personal Information
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            marital_status = request.POST.get('marital_status')
            location = request.POST.get('location')
            education_level = request.POST.get('education_level')

            # Member Roles
            member_roles = request.POST.getlist('member_roles')
            church_clergy_roles = request.POST.getlist('church_clergy_roles') if 'clergy' in member_roles else []
            special_clergy_roles = request.POST.getlist('special_clergy_roles') if 'clergy' in member_roles else []

            # Ensure regular_member is always included
            if 'regular_member' not in member_roles:
                member_roles.append('regular_member')

            phone_number = request.POST.get('phone_number')
            email_address = request.POST.get('email_address', '')

            # Job Information
            job_occupations = request.POST.getlist('job_occupations')

            # Baptismal Information
            baptismal_first_name = request.POST.get('baptismal_first_name')
            baptismal_last_name = request.POST.get('baptismal_last_name')
            date_baptized = request.POST.get('date_baptized')
            date_joined_religion = request.POST.get('date_joined_religion')

            # Home Church Structure
            user_home_diocese_id = request.POST.get('user_home_diocese')
            user_home_pastorate_id = request.POST.get('user_home_pastorate')
            user_home_church_id = request.POST.get('user_home_church')

            # Emergency Contacts
            emergency_contact_1_name = request.POST.get('emergency_contact_1_name', '')
            emergency_contact_1_relationship = request.POST.get('emergency_contact_1_relationship', '')
            emergency_contact_1_phone = request.POST.get('emergency_contact_1_phone', '')
            emergency_contact_1_email = request.POST.get('emergency_contact_1_email', '')

            emergency_contact_2_name = request.POST.get('emergency_contact_2_name', '')
            emergency_contact_2_relationship = request.POST.get('emergency_contact_2_relationship', '')
            emergency_contact_2_phone = request.POST.get('emergency_contact_2_phone', '')
            emergency_contact_2_email = request.POST.get('emergency_contact_2_email', '')

            # Profile Photo
            profile_photo = request.FILES.get('profile_photo')
            profile_photo_url = request.POST.get('profile_photo_url', '').strip()

            # Custom Fields
            custom_field_names = request.POST.getlist('custom_field_names[]')
            custom_field_values = request.POST.getlist('custom_field_values[]')
            custom_fields = {}
            for name, value in zip(custom_field_names, custom_field_values):
                if name and value:  # Only add non-empty fields
                    custom_fields[name] = value

            # New Fields
            membership_status = request.POST.get('membership_status', 'Active')
            is_pwd = request.POST.get('is_pwd') == 'Yes'
            pwd_type = request.POST.get('pwd_type', '') if is_pwd else ''
            pwd_other_description = request.POST.get('pwd_other_description', '')
            is_staff = request.POST.get('is_staff') == 'Yes'
            is_ordained = request.POST.get('is_ordained') == 'Yes'

            # Family Details (optional)
            father_id = request.POST.get('father') or None
            mother_id = request.POST.get('mother') or None
            guardian_id = request.POST.get('guardian') or None
            brother_id = request.POST.get('brother') or None
            sister_id = request.POST.get('sister') or None
            uncle_id = request.POST.get('uncle') or None
            aunt_id = request.POST.get('aunt') or None
            friend_id = request.POST.get('friend') or None

            # Town Church Structure (Optional)
            user_town_diocese_id = request.POST.get('user_town_diocese') or None
            user_town_pastorate_id = request.POST.get('user_town_pastorate') or None
            user_town_church_id = request.POST.get('user_town_church') or None

            # Validation
            required_fields = [
                first_name, last_name, username, gender, date_of_birth,
                marital_status, location, education_level, phone_number, 
                baptismal_first_name, baptismal_last_name, 
                date_baptized, date_joined_religion, user_home_diocese_id, 
                user_home_pastorate_id, user_home_church_id
            ]

            # Job occupations are optional

            if not all(required_fields):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('members:add_member')

            # Check username uniqueness
            if Member.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return redirect('members:add_member')
            
            # Check phone number uniqueness
            if Member.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Phone number already exists. Please use a different phone number.')
                return redirect('members:add_member')
            
            # Check email uniqueness if provided
            if email_address and Member.objects.filter(email_address=email_address).exists():
                messages.error(request, 'Email address already exists. Please use a different email address.')
                return redirect('members:add_member')

            # Get related objects
            user_home_diocese = Diocese.objects.get(id=user_home_diocese_id)
            user_home_pastorate = Pastorate.objects.get(id=user_home_pastorate_id)
            user_home_church = Church.objects.get(id=user_home_church_id)

            user_town_diocese = Diocese.objects.get(id=user_town_diocese_id) if user_town_diocese_id else None
            user_town_pastorate = Pastorate.objects.get(id=user_town_pastorate_id) if user_town_pastorate_id else None
            user_town_church = Church.objects.get(id=user_town_church_id) if user_town_church_id else None

            # Create member
            member = Member.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                gender=gender,
                date_of_birth=date_of_birth,
                marital_status=marital_status,
                location=location,
                education_level=education_level,
                member_roles=member_roles,
                church_clergy_roles=church_clergy_roles,
                special_clergy_roles=special_clergy_roles,
                phone_number=phone_number,
                email_address=email_address,
                job_occupations=job_occupations,
                baptismal_first_name=baptismal_first_name,
                baptismal_last_name=baptismal_last_name,
                date_baptized=date_baptized,
                date_joined_religion=date_joined_religion,
                user_home_diocese=user_home_diocese,
                user_home_pastorate=user_home_pastorate,
                user_home_church=user_home_church,
                user_town_diocese=user_town_diocese,
                user_town_pastorate=user_town_pastorate,
                user_town_church=user_town_church,
                # Emergency Contacts
                emergency_contact_1_name=emergency_contact_1_name,
                emergency_contact_1_relationship=emergency_contact_1_relationship,
                emergency_contact_1_phone=emergency_contact_1_phone,
                emergency_contact_1_email=emergency_contact_1_email,
                emergency_contact_2_name=emergency_contact_2_name,
                emergency_contact_2_relationship=emergency_contact_2_relationship,
                emergency_contact_2_phone=emergency_contact_2_phone,
                emergency_contact_2_email=emergency_contact_2_email,
                # Profile Photo
                profile_photo=profile_photo,
                profile_photo_url=profile_photo_url,
                # Custom Fields
                custom_fields=custom_fields,
                # New Fields
                membership_status=membership_status,
                is_pwd=is_pwd,
                pwd_type=pwd_type,
                pwd_other_description=pwd_other_description,
                is_staff=is_staff,
                is_ordained=is_ordained,
                # Family Details
                father_id=father_id,
                mother_id=mother_id,
                guardian_id=guardian_id,
                brother_id=brother_id,
                sister_id=sister_id,
                uncle_id=uncle_id,
                aunt_id=aunt_id,
                friend_id=friend_id,
            )

            # Handle document uploads
            document_types = request.POST.getlist('document_types[]')
            document_titles = request.POST.getlist('document_titles[]')
            document_descriptions = request.POST.getlist('document_descriptions[]')
            document_files = request.FILES.getlist('document_files[]')

            for i, (doc_type, title, description, file) in enumerate(zip(document_types, document_titles, document_descriptions, document_files)):
                if doc_type and title and file:  # Only process if all required fields are present
                    MemberDocument.objects.create(
                        member=member,
                        document_type=doc_type,
                        title=title,
                        description=description,
                        document_file=file,
                        uploaded_by=f"Admin Registration"  # Could be improved with user authentication
                    )

            messages.success(request, f'Member "{member.full_name}" has been successfully registered!')
            return redirect('members:index')

        except Exception as e:
            messages.error(request, f'Error creating member: {str(e)}')
            return redirect('members:add_member')

# API endpoints for cascading dropdowns
@login_required
def get_pastorates_by_diocese(request, diocese_id):
    """Get pastorates for a specific diocese"""
    try:
        pastorates = Pastorate.objects.filter(
            diocese_id=diocese_id, 
            is_active=True
        ).select_related('diocese').values('id', 'name').order_by('name')
        return JsonResponse(list(pastorates), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_churches_by_pastorate(request, pastorate_id):
    """Get churches for a specific pastorate"""
    try:
        churches = Church.objects.filter(
            pastorate_id=pastorate_id, 
            is_active=True
        ).select_related('pastorate').values('id', 'name').order_by('name')
        return JsonResponse(list(churches), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def member_detail(request, username):
    """View member details"""
    member = get_object_or_404(Member, username=username)
    context = {
        'page_title': f'Member Details - {member.full_name}',
        'member': member,
    }
    return render(request, 'members/member_detail.html', context)

@login_required
def search_members_api(request):
    """API endpoint to search members for family relationships"""
    search_term = request.GET.get('q', '').strip()
    if len(search_term) < 2:
        return JsonResponse([], safe=False)

    members = Member.objects.filter(
        Q(username__icontains=search_term) |
        Q(first_name__icontains=search_term) |
        Q(last_name__icontains=search_term) |
        Q(phone_number__icontains=search_term) |
        Q(email_address__icontains=search_term)
    ).exclude(membership_status__in=['Left/Quit', 'Dead'])[:10]

    results = []
    for member in members:
        results.append({
            'id': member.id,
            'username': member.username,
            'name': member.full_name,
            'phone': member.phone_number,
            'email': member.email_address,
            'display': f"{member.full_name} ({member.username}) - {member.phone_number}"
        })

    return JsonResponse(results, safe=False)