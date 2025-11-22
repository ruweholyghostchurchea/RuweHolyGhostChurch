"""
Views for Visitors app - Church Visitor Management System
All views are mobile-responsive and include proper permissions.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Visitor, VisitorVisit, VisitorFollowUp
from .forms import VisitorForm, VisitorVisitForm, VisitorFollowUpForm, ConvertToMemberForm
from .utils import calculate_visitor_statistics
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese


@login_required
def index(request):
    """
    Visitors dashboard/home page with quick stats and recent visitors.
    Mobile-responsive layout with cards for statistics.
    """
    # Get recent visitors (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_visitors = Visitor.objects.filter(
        first_visit_date__gte=thirty_days_ago
    ).order_by('-first_visit_date')[:10]
    
    # Calculate quick statistics
    total_visitors = Visitor.objects.filter(is_active=True).count()
    visitors_this_month = Visitor.objects.filter(
        first_visit_date__month=timezone.now().month,
        first_visit_date__year=timezone.now().year
    ).count()
    converted_count = Visitor.objects.filter(converted_to_member=True).count()
    interested_in_membership = Visitor.objects.filter(
        interested_in_membership=True,
        converted_to_member=False,
        is_active=True
    ).count()
    
    context = {
        'page_title': 'Visitors Management',
        'recent_visitors': recent_visitors,
        'total_visitors': total_visitors,
        'visitors_this_month': visitors_this_month,
        'converted_count': converted_count,
        'interested_in_membership': interested_in_membership,
    }
    return render(request, 'visitors/index.html', context)


@login_required
def visitor_list(request):
    """
    List all visitors with search and filter capabilities.
    Includes pagination for large datasets.
    Mobile-responsive table with search filters.
    """
    # Start with all active visitors
    visitors = Visitor.objects.filter(is_active=True).select_related(
        'church', 'pastorate', 'diocese'
    ).order_by('-first_visit_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        visitors = visitors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(identifier__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email_address__icontains=search_query)
        )
    
    # Filter by church hierarchy
    church_id = request.GET.get('church')
    if church_id:
        visitors = visitors.filter(church_id=church_id)
    
    pastorate_id = request.GET.get('pastorate')
    if pastorate_id:
        visitors = visitors.filter(pastorate_id=pastorate_id)
    
    diocese_id = request.GET.get('diocese')
    if diocese_id:
        visitors = visitors.filter(diocese_id=diocese_id)
    
    is_dean = request.GET.get('is_dean')
    if is_dean == '1':
        visitors = visitors.filter(is_dean_visitor=True)
    
    # Filter by conversion status
    converted = request.GET.get('converted')
    if converted == '1':
        visitors = visitors.filter(converted_to_member=True)
    elif converted == '0':
        visitors = visitors.filter(converted_to_member=False)
    
    # Filter by membership interest
    interested = request.GET.get('interested')
    if interested == '1':
        visitors = visitors.filter(interested_in_membership=True, converted_to_member=False)
    
    # Pagination (20 visitors per page)
    paginator = Paginator(visitors, 20)
    page_number = request.GET.get('page')
    visitors_page = paginator.get_page(page_number)
    
    # Get filter options for dropdowns
    churches = Church.objects.all().order_by('name')
    pastorates = Pastorate.objects.all().order_by('name')
    dioceses = Diocese.objects.all().order_by('name')
    
    context = {
        'page_title': 'All Visitors',
        'visitors': visitors_page,
        'search_query': search_query,
        'churches': churches,
        'pastorates': pastorates,
        'dioceses': dioceses,
        'total_count': paginator.count,
    }
    return render(request, 'visitors/visitor_list.html', context)


@login_required
def visitor_add(request):
    """
    Add a new visitor to the system.
    On successful save, welcome email is sent automatically via signal.
    """
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.created_by = request.user
            visitor.save()
            
            messages.success(request, f'Visitor {visitor.full_name} added successfully!')
            
            # If email provided, notify about welcome email
            if visitor.email_address:
                messages.info(request, 'Welcome email will be sent to the visitor.')
            
            # Redirect to visitor detail page
            return redirect('visitors:visitor_detail', visitor_id=visitor.id)
    else:
        form = VisitorForm()
    
    context = {
        'page_title': 'Add New Visitor',
        'form': form,
        'action': 'Add'
    }
    return render(request, 'visitors/visitor_form.html', context)


@login_required
def visitor_detail(request, visitor_id):
    """
    View detailed information about a specific visitor.
    Shows visitor info, all visits, follow-ups, and conversion status.
    """
    visitor = get_object_or_404(
        Visitor.objects.select_related('church', 'pastorate', 'diocese', 'member_profile'),
        id=visitor_id
    )
    
    # Get all visits for this visitor
    visits = visitor.visits.all().order_by('-visit_date')
    
    # Get all follow-ups for this visitor
    follow_ups = visitor.follow_ups.all().order_by('-follow_up_date')
    
    context = {
        'page_title': f'Visitor: {visitor.full_name}',
        'visitor': visitor,
        'visits': visits,
        'follow_ups': follow_ups,
    }
    return render(request, 'visitors/visitor_detail.html', context)


@login_required
def visitor_edit(request, visitor_id):
    """
    Edit an existing visitor's information.
    Pre-populates form with current visitor data.
    """
    visitor = get_object_or_404(Visitor, id=visitor_id)
    
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Visitor {visitor.full_name} updated successfully!')
            return redirect('visitors:visitor_detail', visitor_id=visitor.id)
    else:
        form = VisitorForm(instance=visitor)
    
    context = {
        'page_title': f'Edit Visitor: {visitor.full_name}',
        'form': form,
        'visitor': visitor,
        'action': 'Update'
    }
    return render(request, 'visitors/visitor_form.html', context)


@login_required
def visitor_delete(request, visitor_id):
    """
    Soft delete a visitor (mark as inactive).
    POST request required for security.
    """
    if request.method == 'POST':
        visitor = get_object_or_404(Visitor, id=visitor_id)
        visitor.is_active = False
        visitor.save()
        messages.success(request, f'Visitor {visitor.full_name} removed from active list.')
        return redirect('visitors:visitor_list')
    
    # If GET request, redirect to detail page
    return redirect('visitors:visitor_detail', visitor_id=visitor_id)


@login_required
def register_visit(request, visitor_id):
    """
    Register a subsequent visit (2nd, 3rd, etc.) for a visitor.
    Automatically calculates visit number and sends thank you email via signal.
    """
    visitor = get_object_or_404(Visitor, id=visitor_id)
    
    # Calculate next visit number
    latest_visit = visitor.visits.order_by('-visit_number').first()
    next_visit_number = latest_visit.visit_number + 1 if latest_visit else 2
    
    if request.method == 'POST':
        form = VisitorVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.visitor = visitor
            visit.created_by = request.user
            visit.save()
            
            messages.success(
                request,
                f'Visit #{visit.visit_number} registered for {visitor.full_name}!'
            )
            
            # Notify about email
            if visitor.email_address:
                messages.info(request, 'Thank you email will be sent to the visitor.')
            
            return redirect('visitors:visitor_detail', visitor_id=visitor.id)
    else:
        # Pre-fill visit number
        form = VisitorVisitForm(initial={'visit_number': next_visit_number})
    
    context = {
        'page_title': f'Register Visit for {visitor.full_name}',
        'form': form,
        'visitor': visitor,
        'next_visit_number': next_visit_number,
    }
    return render(request, 'visitors/register_visit.html', context)


@login_required
def record_followup(request, visitor_id):
    """
    Record a follow-up attempt/contact with a visitor.
    Tracks follow-up method, status, and outcomes.
    """
    visitor = get_object_or_404(Visitor, id=visitor_id)
    
    if request.method == 'POST':
        form = VisitorFollowUpForm(request.POST)
        if form.is_valid():
            follow_up = form.save(commit=False)
            follow_up.visitor = visitor
            follow_up.created_by = request.user
            follow_up.save()
            
            messages.success(request, f'Follow-up recorded for {visitor.full_name}!')
            return redirect('visitors:visitor_detail', visitor_id=visitor.id)
    else:
        form = VisitorFollowUpForm()
    
    context = {
        'page_title': f'Record Follow-up for {visitor.full_name}',
        'form': form,
        'visitor': visitor,
    }
    return render(request, 'visitors/record_followup.html', context)


@login_required
def convert_to_member(request, visitor_id):
    """
    Convert a visitor to a church member.
    Opens member registration form with visitor data pre-populated.
    """
    visitor = get_object_or_404(Visitor, id=visitor_id)
    
    # Check if already converted
    if visitor.converted_to_member:
        messages.warning(request, 'This visitor has already been converted to a member.')
        return redirect('visitors:visitor_detail', visitor_id=visitor.id)
    
    if request.method == 'POST':
        form = ConvertToMemberForm(request.POST)
        if form.is_valid():
            # Create new member with visitor data
            member = Member()
            member.first_name = visitor.first_name
            member.last_name = visitor.last_name
            member.gender = visitor.gender
            member.date_of_birth = visitor.date_of_birth
            member.phone_number = visitor.phone_number
            member.email_address = visitor.email_address
            member.physical_address = visitor.physical_address
            member.user_home_church = visitor.church
            member.created_by = request.user
            member.save()
            
            # Update visitor record
            visitor.converted_to_member = True
            visitor.converted_date = timezone.now().date()
            visitor.member_profile = member
            visitor.is_active = False  # Remove from active visitors
            visitor.save()
            
            messages.success(
                request,
                f'{visitor.full_name} has been successfully converted to a member!'
            )
            return redirect('members:member_detail', member_id=member.id)
    else:
        # Pre-fill form with visitor data
        form = ConvertToMemberForm(initial={
            'first_name': visitor.first_name,
            'last_name': visitor.last_name,
            'gender': visitor.gender,
            'date_of_birth': visitor.date_of_birth,
            'phone_number': visitor.phone_number,
            'email_address': visitor.email_address,
            'physical_address': visitor.physical_address,
        })
    
    context = {
        'page_title': f'Convert {visitor.full_name} to Member',
        'form': form,
        'visitor': visitor,
    }
    return render(request, 'visitors/convert_to_member.html', context)


@login_required
def visitor_statistics(request):
    """
    Display visitor statistics and demographics dashboard.
    Shows data across church hierarchy with charts and graphs.
    Mobile-responsive dashboard with filter options.
    """
    # Get filter parameters
    level = request.GET.get('level', 'church')
    church_id = request.GET.get('church')
    pastorate_id = request.GET.get('pastorate')
    diocese_id = request.GET.get('diocese')
    
    # Date range filters (default: last 30 days)
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if not date_from:
        date_from = (timezone.now().date() - timedelta(days=30)).isoformat()
    if not date_to:
        date_to = timezone.now().date().isoformat()
    
    # Convert date strings to date objects
    start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
    end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
    
    # Get statistics based on hierarchy level
    church = None
    pastorate = None
    diocese = None
    
    if level == 'church' and church_id:
        church = get_object_or_404(Church, id=church_id)
    elif level == 'pastorate' and pastorate_id:
        pastorate = get_object_or_404(Pastorate, id=pastorate_id)
    elif level == 'diocese' and diocese_id:
        diocese = get_object_or_404(Diocese, id=diocese_id)
    
    # Calculate statistics using utility function
    stats = calculate_visitor_statistics(
        level=level,
        church=church,
        pastorate=pastorate,
        diocese=diocese,
        start_date=start_date,
        end_date=end_date
    )
    
    # Get hierarchy options for filters
    churches = Church.objects.all().order_by('name')
    pastorates = Pastorate.objects.all().order_by('name')
    dioceses = Diocese.objects.all().order_by('name')
    
    context = {
        'page_title': 'Visitor Statistics & Demographics',
        'stats': stats,
        'level': level,
        'selected_church': church,
        'selected_pastorate': pastorate,
        'selected_diocese': diocese,
        'churches': churches,
        'pastorates': pastorates,
        'dioceses': dioceses,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'visitors/statistics.html', context)
