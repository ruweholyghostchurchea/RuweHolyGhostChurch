from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Member, MemberDocument
from church_structure.models import Diocese, Pastorate, Church
import json
from datetime import datetime

@login_required
def index(request):
    """Members main view with search and pagination"""
    search_query = request.GET.get('search', '')
    user_group_filter = request.GET.get('user_group', '')
    diocese_filter = request.GET.get('diocese', '')

    members = Member.objects.exclude(membership_status__in=['Left/Quit', 'Dead']).select_related(
        'user_home_diocese', 'user_home_pastorate', 'user_home_church',
        'user_town_diocese', 'user_town_pastorate', 'user_town_church'
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
        'clergy_count': active_members.filter(member_roles__contains=['clergy']).count(),
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
            date_of_birth_str = request.POST.get('date_of_birth')
            marital_status = request.POST.get('marital_status')
            location = request.POST.get('location')
            education_level = request.POST.get('education_level')

            # Convert date strings to date objects
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date() if date_of_birth_str else None
            except ValueError:
                messages.error(request, 'Invalid date of birth format. Please use YYYY-MM-DD format.')
                return redirect('members:add_member')

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
            date_baptized_str = request.POST.get('date_baptized')
            date_joined_religion_str = request.POST.get('date_joined_religion')

            # Convert baptismal date strings to date objects
            try:
                date_baptized = datetime.strptime(date_baptized_str, '%Y-%m-%d').date() if date_baptized_str else None
                date_joined_religion = datetime.strptime(date_joined_religion_str, '%Y-%m-%d').date() if date_joined_religion_str else None
            except ValueError:
                messages.error(request, 'Invalid baptismal or religion date format. Please use YYYY-MM-DD format.')
                return redirect('members:add_member')

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

            # Family Details (optional) - Parse from form
            fathers = []
            father_names = request.POST.getlist('father_name[]')
            father_types = request.POST.getlist('father_type[]')
            father_is_members = request.POST.getlist('father_is_member[]')
            father_identifiers = request.POST.getlist('father_identifier[]')
            father_phones = request.POST.getlist('father_phone[]')
            father_alives = request.POST.getlist('father_alive[]')

            for i, name in enumerate(father_names):
                if name.strip():
                    fathers.append({
                        'name': name.strip(),
                        'relationship_type': father_types[i] if i < len(father_types) else 'biological',
                        'alive': father_alives[i] == 'yes' if i < len(father_alives) else True,
                        'is_member': father_is_members[i] == 'yes' if i < len(father_is_members) else False,
                        'member_identifier': father_identifiers[i].strip() if i < len(father_identifiers) and father_is_members[i] == 'yes' else '',
                        'phone': father_phones[i].strip() if i < len(father_phones) else ''
                    })

            mothers = []
            mother_names = request.POST.getlist('mother_name[]')
            mother_types = request.POST.getlist('mother_type[]')
            mother_is_members = request.POST.getlist('mother_is_member[]')
            mother_identifiers = request.POST.getlist('mother_identifier[]')
            mother_phones = request.POST.getlist('mother_phone[]')
            mother_alives = request.POST.getlist('mother_alive[]')

            for i, name in enumerate(mother_names):
                if name.strip():
                    mothers.append({
                        'name': name.strip(),
                        'relationship_type': mother_types[i] if i < len(mother_types) else 'biological',
                        'alive': mother_alives[i] == 'yes' if i < len(mother_alives) else True,
                        'is_member': mother_is_members[i] == 'yes' if i < len(mother_is_members) else False,
                        'member_identifier': mother_identifiers[i].strip() if i < len(mother_identifiers) and mother_is_members[i] == 'yes' else '',
                        'phone': mother_phones[i].strip() if i < len(mother_phones) else ''
                    })

            spouse = {}
            spouse_names = request.POST.getlist('spouse_name[]')
            spouse_is_members = request.POST.getlist('spouse_is_member[]')
            spouse_identifiers = request.POST.getlist('spouse_identifier[]')
            spouse_phones = request.POST.getlist('spouse_phone[]')
            spouse_alives = request.POST.getlist('spouse_alive[]')

            if spouse_names and spouse_names[0].strip():
                spouse = {
                    'name': spouse_names[0].strip(),
                    'alive': spouse_alives[0] == 'yes' if spouse_alives else True,
                    'is_member': spouse_is_members[0] == 'yes' if spouse_is_members else False,
                    'member_identifier': spouse_identifiers[0].strip() if spouse_identifiers and spouse_is_members and spouse_is_members[0] == 'yes' else '',
                    'phone': spouse_phones[0].strip() if spouse_phones else ''
                }

            guardians = []
            guardian_names = request.POST.getlist('guardian_name[]')
            guardian_is_members = request.POST.getlist('guardian_is_member[]')
            guardian_identifiers = request.POST.getlist('guardian_identifier[]')
            guardian_phones = request.POST.getlist('guardian_phone[]')

            for i, name in enumerate(guardian_names):
                if name.strip():
                    guardians.append({
                        'name': name.strip(),
                        'is_member': guardian_is_members[i] == 'yes' if i < len(guardian_is_members) else False,
                        'member_identifier': guardian_identifiers[i].strip() if i < len(guardian_identifiers) and guardian_is_members[i] == 'yes' else '',
                        'phone': guardian_phones[i].strip() if i < len(guardian_phones) else ''
                    })

            brothers = []
            brother_names = request.POST.getlist('brother_name[]')
            brother_is_members = request.POST.getlist('brother_is_member[]')
            brother_identifiers = request.POST.getlist('brother_identifier[]')
            brother_phones = request.POST.getlist('brother_phone[]')

            for i, name in enumerate(brother_names):
                if name.strip():
                    brothers.append({
                        'name': name.strip(),
                        'is_member': brother_is_members[i] == 'yes' if i < len(brother_is_members) else False,
                        'member_identifier': brother_identifiers[i].strip() if i < len(brother_identifiers) and brother_is_members[i] == 'yes' else '',
                        'phone': brother_phones[i].strip() if i < len(brother_phones) else ''
                    })

            sisters = []
            sister_names = request.POST.getlist('sister_name[]')
            sister_is_members = request.POST.getlist('sister_is_member[]')
            sister_identifiers = request.POST.getlist('sister_identifier[]')
            sister_phones = request.POST.getlist('sister_phone[]')

            for i, name in enumerate(sister_names):
                if name.strip():
                    sisters.append({
                        'name': name.strip(),
                        'is_member': sister_is_members[i] == 'yes' if i < len(sister_is_members) else False,
                        'member_identifier': sister_identifiers[i].strip() if i < len(sister_identifiers) and sister_is_members[i] == 'yes' else '',
                        'phone': sister_phones[i].strip() if i < len(sister_phones) else ''
                    })

            uncles = []
            uncle_names = request.POST.getlist('uncle_name[]')
            uncle_is_members = request.POST.getlist('uncle_is_member[]')
            uncle_identifiers = request.POST.getlist('uncle_identifier[]')
            uncle_phones = request.POST.getlist('uncle_phone[]')

            for i, name in enumerate(uncle_names):
                if name.strip():
                    uncles.append({
                        'name': name.strip(),
                        'is_member': uncle_is_members[i] == 'yes' if i < len(uncle_is_members) else False,
                        'member_identifier': uncle_identifiers[i].strip() if i < len(uncle_identifiers) and uncle_is_members[i] == 'yes' else '',
                        'phone': uncle_phones[i].strip() if i < len(uncle_phones) else ''
                    })

            aunts = []
            aunt_names = request.POST.getlist('aunt_name[]')
            aunt_is_members = request.POST.getlist('aunt_is_member[]')
            aunt_identifiers = request.POST.getlist('aunt_identifier[]')
            aunt_phones = request.POST.getlist('aunt_phone[]')

            for i, name in enumerate(aunt_names):
                if name.strip():
                    aunts.append({
                        'name': name.strip(),
                        'is_member': aunt_is_members[i] == 'yes' if i < len(aunt_is_members) else False,
                        'member_identifier': aunt_identifiers[i].strip() if i < len(aunt_identifiers) and aunt_is_members[i] == 'yes' else '',
                        'phone': aunt_phones[i].strip() if i < len(aunt_phones) else ''
                    })

            friends = []
            friend_names = request.POST.getlist('friend_name[]')
            friend_is_members = request.POST.getlist('friend_is_member[]')
            friend_identifiers = request.POST.getlist('friend_identifier[]')
            friend_phones = request.POST.getlist('friend_phone[]')

            for i, name in enumerate(friend_names):
                if name.strip():
                    friends.append({
                        'name': name.strip(),
                        'is_member': friend_is_members[i] == 'yes' if i < len(friend_is_members) else False,
                        'member_identifier': friend_identifiers[i].strip() if i < len(friend_identifiers) and friend_is_members[i] == 'yes' else '',
                        'phone': friend_phones[i].strip() if i < len(friend_phones) else ''
                    })

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
                fathers=fathers,
                mothers=mothers,
                spouse=spouse,
                guardians=guardians,
                brothers=brothers,
                sisters=sisters,
                uncles=uncles,
                aunts=aunts,
                friends=friends,
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
def edit_member(request, username):
    """Edit existing member view"""
    member = get_object_or_404(Member, username=username)

    if request.method == 'GET':
        dioceses = Diocese.objects.filter(is_active=True).order_by('country', 'name')
        context = {
            'page_title': f'Edit Member - {member.full_name}',
            'member': member,
            'dioceses': dioceses,
            'membership_statuses': Member.MEMBERSHIP_STATUS_CHOICES,
            'pwd_types': Member.PWD_TYPE_CHOICES,
            'member_roles': Member.MEMBER_ROLES,
            'church_clergy_roles': Member.CHURCH_CLERGY_ROLES,
            'special_clergy_roles': Member.SPECIAL_CLERGY_ROLES,
            'job_categories': Member.JOB_CATEGORIES,
            'job_choices': Member.JOB_CHOICES,
        }
        return render(request, 'members/edit_member.html', context)

    elif request.method == 'POST':
        try:
            # Personal Information
            member.first_name = request.POST.get('first_name')
            member.last_name = request.POST.get('last_name')
            new_username = request.POST.get('username')
            member.gender = request.POST.get('gender')
            date_of_birth_str = request.POST.get('date_of_birth')
            member.marital_status = request.POST.get('marital_status')
            member.location = request.POST.get('location')
            member.education_level = request.POST.get('education_level')

            # Check username uniqueness if changed
            if new_username != member.username:
                if Member.objects.filter(username=new_username).exists():
                    messages.error(request, 'Username already exists. Please choose a different username.')
                    return redirect('members:edit_member', username=username)
                member.username = new_username

            # Convert date strings to date objects
            try:
                member.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date() if date_of_birth_str else None
            except ValueError:
                messages.error(request, 'Invalid date of birth format. Please use YYYY-MM-DD format.')
                return redirect('members:edit_member', username=username)

            # Member Roles
            member_roles = request.POST.getlist('member_roles')
            church_clergy_roles = request.POST.getlist('church_clergy_roles') if 'clergy' in member_roles else []
            special_clergy_roles = request.POST.getlist('special_clergy_roles') if 'clergy' in member_roles else []

            # Ensure regular_member is always included
            if 'regular_member' not in member_roles:
                member_roles.append('regular_member')

            member.member_roles = member_roles
            member.church_clergy_roles = church_clergy_roles
            member.special_clergy_roles = special_clergy_roles

            phone_number = request.POST.get('phone_number')
            email_address = request.POST.get('email_address', '')

            # Check phone number uniqueness if changed
            if phone_number != member.phone_number:
                if Member.objects.filter(phone_number=phone_number).exists():
                    messages.error(request, 'Phone number already exists. Please use a different phone number.')
                    return redirect('members:edit_member', username=username)
                member.phone_number = phone_number

            # Check email uniqueness if changed
            if email_address != member.email_address:
                if email_address and Member.objects.filter(email_address=email_address).exists():
                    messages.error(request, 'Email address already exists. Please use a different email address.')
                    return redirect('members:edit_member', username=username)
                member.email_address = email_address

            # Job Information
            member.job_occupations = request.POST.getlist('job_occupations')
            member.income_details = request.POST.get('income_details', '')

            # Baptismal Information
            member.baptismal_first_name = request.POST.get('baptismal_first_name')
            member.baptismal_last_name = request.POST.get('baptismal_last_name')
            date_baptized_str = request.POST.get('date_baptized')
            date_joined_religion_str = request.POST.get('date_joined_religion')

            # Convert baptismal date strings to date objects
            try:
                member.date_baptized = datetime.strptime(date_baptized_str, '%Y-%m-%d').date() if date_baptized_str else None
                member.date_joined_religion = datetime.strptime(date_joined_religion_str, '%Y-%m-%d').date() if date_joined_religion_str else None
            except ValueError:
                messages.error(request, 'Invalid baptismal or religion date format. Please use YYYY-MM-DD format.')
                return redirect('members:edit_member', username=username)

            # Home Church Structure
            user_home_diocese_id = request.POST.get('user_home_diocese')
            user_home_pastorate_id = request.POST.get('user_home_pastorate')
            user_home_church_id = request.POST.get('user_home_church')

            # Emergency Contacts
            member.emergency_contact_1_name = request.POST.get('emergency_contact_1_name', '')
            member.emergency_contact_1_relationship = request.POST.get('emergency_contact_1_relationship', '')
            member.emergency_contact_1_phone = request.POST.get('emergency_contact_1_phone', '')
            member.emergency_contact_1_email = request.POST.get('emergency_contact_1_email', '')

            member.emergency_contact_2_name = request.POST.get('emergency_contact_2_name', '')
            member.emergency_contact_2_relationship = request.POST.get('emergency_contact_2_relationship', '')
            member.emergency_contact_2_phone = request.POST.get('emergency_contact_2_phone', '')
            member.emergency_contact_2_email = request.POST.get('emergency_contact_2_email', '')

            # Profile Photo
            profile_photo = request.FILES.get('profile_photo')
            profile_photo_url = request.POST.get('profile_photo_url', '').strip()

            if profile_photo:
                member.profile_photo = profile_photo
            if profile_photo_url:
                member.profile_photo_url = profile_photo_url

            # Custom Fields
            custom_field_names = request.POST.getlist('custom_field_names[]')
            custom_field_values = request.POST.getlist('custom_field_values[]')
            custom_fields = {}
            for name, value in zip(custom_field_names, custom_field_values):
                if name and value:  # Only add non-empty fields
                    custom_fields[name] = value
            member.custom_fields = custom_fields

            # New Fields
            member.membership_status = request.POST.get('membership_status', 'Active')
            member.is_pwd = request.POST.get('is_pwd') == 'Yes'
            member.pwd_type = request.POST.get('pwd_type', '') if member.is_pwd else ''
            member.pwd_other_description = request.POST.get('pwd_other_description', '')
            member.is_staff = request.POST.get('is_staff') == 'Yes'
            member.is_ordained = request.POST.get('is_ordained') == 'Yes'

            # Family Details (optional) - Parse from form
            fathers = []
            father_names = request.POST.getlist('father_name[]')
            father_types = request.POST.getlist('father_type[]')
            father_is_members = request.POST.getlist('father_is_member[]')
            father_identifiers = request.POST.getlist('father_identifier[]')
            father_phones = request.POST.getlist('father_phone[]')
            father_alives = request.POST.getlist('father_alive[]')

            for i, name in enumerate(father_names):
                if name.strip():
                    fathers.append({
                        'name': name.strip(),
                        'relationship_type': father_types[i] if i < len(father_types) else 'biological',
                        'alive': father_alives[i] == 'yes' if i < len(father_alives) else True,
                        'is_member': father_is_members[i] == 'yes' if i < len(father_is_members) else False,
                        'member_identifier': father_identifiers[i].strip() if i < len(father_identifiers) and father_is_members[i] == 'yes' else '',
                        'phone': father_phones[i].strip() if i < len(father_phones) else ''
                    })

            mothers = []
            mother_names = request.POST.getlist('mother_name[]')
            mother_types = request.POST.getlist('mother_type[]')
            mother_is_members = request.POST.getlist('mother_is_member[]')
            mother_identifiers = request.POST.getlist('mother_identifier[]')
            mother_phones = request.POST.getlist('mother_phone[]')
            mother_alives = request.POST.getlist('mother_alive[]')

            for i, name in enumerate(mother_names):
                if name.strip():
                    mothers.append({
                        'name': name.strip(),
                        'relationship_type': mother_types[i] if i < len(mother_types) else 'biological',
                        'alive': mother_alives[i] == 'yes' if i < len(mother_alives) else True,
                        'is_member': mother_is_members[i] == 'yes' if i < len(mother_is_members) else False,
                        'member_identifier': mother_identifiers[i].strip() if i < len(mother_identifiers) and mother_is_members[i] == 'yes' else '',
                        'phone': mother_phones[i].strip() if i < len(mother_phones) else ''
                    })

            spouse = {}
            spouse_names = request.POST.getlist('spouse_name[]')
            spouse_is_members = request.POST.getlist('spouse_is_member[]')
            spouse_identifiers = request.POST.getlist('spouse_identifier[]')
            spouse_phones = request.POST.getlist('spouse_phone[]')
            spouse_alives = request.POST.getlist('spouse_alive[]')

            if spouse_names and spouse_names[0].strip():
                spouse = {
                    'name': spouse_names[0].strip(),
                    'alive': spouse_alives[0] == 'yes' if spouse_alives else True,
                    'is_member': spouse_is_members[0] == 'yes' if spouse_is_members else False,
                    'member_identifier': spouse_identifiers[0].strip() if spouse_identifiers and spouse_is_members and spouse_is_members[0] == 'yes' else '',
                    'phone': spouse_phones[0].strip() if spouse_phones else ''
                }

            guardians = []
            guardian_names = request.POST.getlist('guardian_name[]')
            guardian_is_members = request.POST.getlist('guardian_is_member[]')
            guardian_identifiers = request.POST.getlist('guardian_identifier[]')
            guardian_phones = request.POST.getlist('guardian_phone[]')

            for i, name in enumerate(guardian_names):
                if name.strip():
                    guardians.append({
                        'name': name.strip(),
                        'is_member': guardian_is_members[i] == 'yes' if i < len(guardian_is_members) else False,
                        'member_identifier': guardian_identifiers[i].strip() if i < len(guardian_identifiers) and guardian_is_members[i] == 'yes' else '',
                        'phone': guardian_phones[i].strip() if i < len(guardian_phones) else ''
                    })

            brothers = []
            brother_names = request.POST.getlist('brother_name[]')
            brother_is_members = request.POST.getlist('brother_is_member[]')
            brother_identifiers = request.POST.getlist('brother_identifier[]')
            brother_phones = request.POST.getlist('brother_phone[]')

            for i, name in enumerate(brother_names):
                if name.strip():
                    brothers.append({
                        'name': name.strip(),
                        'is_member': brother_is_members[i] == 'yes' if i < len(brother_is_members) else False,
                        'member_identifier': brother_identifiers[i].strip() if i < len(brother_identifiers) and brother_is_members[i] == 'yes' else '',
                        'phone': brother_phones[i].strip() if i < len(brother_phones) else ''
                    })

            sisters = []
            sister_names = request.POST.getlist('sister_name[]')
            sister_is_members = request.POST.getlist('sister_is_member[]')
            sister_identifiers = request.POST.getlist('sister_identifier[]')
            sister_phones = request.POST.getlist('sister_phone[]')

            for i, name in enumerate(sister_names):
                if name.strip():
                    sisters.append({
                        'name': name.strip(),
                        'is_member': sister_is_members[i] == 'yes' if i < len(sister_is_members) else False,
                        'member_identifier': sister_identifiers[i].strip() if i < len(sister_identifiers) and sister_is_members[i] == 'yes' else '',
                        'phone': sister_phones[i].strip() if i < len(sister_phones) else ''
                    })

            uncles = []
            uncle_names = request.POST.getlist('uncle_name[]')
            uncle_is_members = request.POST.getlist('uncle_is_member[]')
            uncle_identifiers = request.POST.getlist('uncle_identifier[]')
            uncle_phones = request.POST.getlist('uncle_phone[]')

            for i, name in enumerate(uncle_names):
                if name.strip():
                    uncles.append({
                        'name': name.strip(),
                        'is_member': uncle_is_members[i] == 'yes' if i < len(uncle_is_members) else False,
                        'member_identifier': uncle_identifiers[i].strip() if i < len(uncle_identifiers) and uncle_is_members[i] == 'yes' else '',
                        'phone': uncle_phones[i].strip() if i < len(uncle_phones) else ''
                    })

            aunts = []
            aunt_names = request.POST.getlist('aunt_name[]')
            aunt_is_members = request.POST.getlist('aunt_is_member[]')
            aunt_identifiers = request.POST.getlist('aunt_identifier[]')
            aunt_phones = request.POST.getlist('aunt_phone[]')

            for i, name in enumerate(aunt_names):
                if name.strip():
                    aunts.append({
                        'name': name.strip(),
                        'is_member': aunt_is_members[i] == 'yes' if i < len(aunt_is_members) else False,
                        'member_identifier': aunt_identifiers[i].strip() if i < len(aunt_identifiers) and aunt_is_members[i] == 'yes' else '',
                        'phone': aunt_phones[i].strip() if i < len(aunt_phones) else ''
                    })

            friends = []
            friend_names = request.POST.getlist('friend_name[]')
            friend_is_members = request.POST.getlist('friend_is_member[]')
            friend_identifiers = request.POST.getlist('friend_identifier[]')
            friend_phones = request.POST.getlist('friend_phone[]')

            for i, name in enumerate(friend_names):
                if name.strip():
                    friends.append({
                        'name': name.strip(),
                        'is_member': friend_is_members[i] == 'yes' if i < len(friend_is_members) else False,
                        'member_identifier': friend_identifiers[i].strip() if i < len(friend_identifiers) and friend_is_members[i] == 'yes' else '',
                        'phone': friend_phones[i].strip() if i < len(friend_phones) else ''
                    })

            member.fathers = fathers
            member.mothers = mothers
            member.spouse = spouse
            member.guardians = guardians
            member.brothers = brothers
            member.sisters = sisters
            member.uncles = uncles
            member.aunts = aunts
            member.friends = friends

            # Town Church Structure (Optional)
            user_town_diocese_id = request.POST.get('user_town_diocese') or None
            user_town_pastorate_id = request.POST.get('user_town_pastorate') or None
            user_town_church_id = request.POST.get('user_town_church') or None

            # Validation for required church structure fields
            required_church_fields = [
                user_home_diocese_id, user_home_pastorate_id, user_home_church_id
            ]

            if not all(required_church_fields):
                messages.error(request, 'Please fill in all required church structure fields (Home Diocese, Pastorate, Church).')
                return redirect('members:edit_member', username=username)

            # Get related objects with error handling
            try:
                member.user_home_diocese = Diocese.objects.get(id=user_home_diocese_id)
                member.user_home_pastorate = Pastorate.objects.get(id=user_home_pastorate_id)
                member.user_home_church = Church.objects.get(id=user_home_church_id)

                member.user_town_diocese = Diocese.objects.get(id=user_town_diocese_id) if user_town_diocese_id else None
                member.user_town_pastorate = Pastorate.objects.get(id=user_town_pastorate_id) if user_town_pastorate_id else None
                member.user_town_church = Church.objects.get(id=user_town_church_id) if user_town_church_id else None
            except (Diocese.DoesNotExist, Pastorate.DoesNotExist, Church.DoesNotExist) as e:
                messages.error(request, f'Invalid church structure selection: {str(e)}')
                return redirect('members:edit_member', username=username)

            # Save the member
            member.save()

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
                        uploaded_by=f"Admin Update"
                    )

            messages.success(request, f'Member "{member.full_name}" has been successfully updated!')
            return redirect('members:member_detail', username=member.username)

        except Exception as e:
            messages.error(request, f'Error updating member: {str(e)}')
            return redirect('members:edit_member', username=username)

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