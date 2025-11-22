"""
Views for Attendance app - Church Attendance/Register Management System
All views are mobile-responsive and include proper permissions.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta

from .models import AttendanceSession, AttendanceRecord, AbsenceStreak, AttendanceStatistics
from .forms import AttendanceSessionForm, AttendanceRecordForm, BulkAttendanceForm, SearchAttendanceForm
from .utils import calculate_attendance_statistics, bulk_mark_attendance
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese


@login_required
def index(request):
    """
    Attendance dashboard/home page with quick stats and upcoming sessions.
    Mobile-responsive layout with cards for statistics.
    """
    # Get upcoming sessions (next 7 days)
    today = timezone.now().date()
    upcoming_sessions = AttendanceSession.objects.filter(
        session_date__gte=today,
        session_date__lte=today + timedelta(days=7),
        is_active=True
    ).order_by('session_date', 'service_time')[:10]
    
    # Get recent sessions (last 30 days)
    recent_sessions = AttendanceSession.objects.filter(
        session_date__gte=today - timedelta(days=30),
        is_active=True
    ).order_by('-session_date', '-service_time')[:5]
    
    # Calculate quick statistics
    total_sessions = AttendanceSession.objects.filter(is_active=True).count()
    sessions_this_month = AttendanceSession.objects.filter(
        session_date__month=today.month,
        session_date__year=today.year,
        is_active=True
    ).count()
    
    # Get members with high absence streaks (3+)
    high_absence_members = AbsenceStreak.objects.filter(
        current_streak__gte=3
    ).select_related('member', 'church').order_by('-current_streak')[:10]
    
    context = {
        'page_title': 'Attendance Management',
        'upcoming_sessions': upcoming_sessions,
        'recent_sessions': recent_sessions,
        'total_sessions': total_sessions,
        'sessions_this_month': sessions_this_month,
        'high_absence_members': high_absence_members,
    }
    return render(request, 'attendance/index.html', context)


@login_required
def session_list(request):
    """
    List all attendance sessions with search and filter capabilities.
    Includes pagination for large datasets.
    Mobile-responsive table with search filters.
    """
    # Start with all active sessions
    sessions = AttendanceSession.objects.filter(
        is_active=True
    ).select_related('church', 'pastorate', 'diocese').order_by('-session_date', '-service_time')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        sessions = sessions.filter(
            Q(session_name__icontains=search_query) |
            Q(session_code__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    if date_from:
        sessions = sessions.filter(session_date__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        sessions = sessions.filter(session_date__lte=date_to)
    
    # Filter by session type
    session_type = request.GET.get('session_type')
    if session_type:
        sessions = sessions.filter(session_type=session_type)
    
    # Filter by hierarchy level
    level = request.GET.get('level')
    if level:
        sessions = sessions.filter(level=level)
    
    # Filter by church
    church_id = request.GET.get('church')
    if church_id:
        sessions = sessions.filter(church_id=church_id)
    
    # Pagination (15 sessions per page)
    paginator = Paginator(sessions, 15)
    page_number = request.GET.get('page')
    sessions_page = paginator.get_page(page_number)
    
    # Get filter form
    search_form = SearchAttendanceForm(request.GET)
    
    context = {
        'page_title': 'All Attendance Sessions',
        'sessions': sessions_page,
        'search_form': search_form,
        'total_count': paginator.count,
    }
    return render(request, 'attendance/session_list.html', context)


@login_required
def session_create(request):
    """
    Create a new attendance session.
    Automatically generates session code and sets up hierarchy.
    """
    if request.method == 'POST':
        form = AttendanceSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            
            messages.success(request, f'Session "{session.session_name}" created successfully!')
            return redirect('attendance:session_detail', session_id=session.id)
    else:
        form = AttendanceSessionForm()
    
    context = {
        'page_title': 'Create Attendance Session',
        'form': form,
        'action': 'Create'
    }
    return render(request, 'attendance/session_form.html', context)


@login_required
def session_detail(request, session_id):
    """
    View detailed information about a specific attendance session.
    Shows session info, attendance records, and statistics.
    """
    session = get_object_or_404(
        AttendanceSession.objects.select_related('church', 'pastorate', 'diocese', 'preacher'),
        id=session_id
    )
    
    # Get all attendance records for this session
    attendance_records = session.attendance_records.select_related('member').order_by('member__last_name', 'member__first_name')
    
    # Calculate statistics
    total_records = attendance_records.count()
    present_count = attendance_records.filter(status='present').count()
    apology_count = attendance_records.filter(status='apology').count()
    absent_count = attendance_records.filter(status='absent').count()
    
    # Calculate percentage
    attendance_rate = 0
    if total_records > 0:
        attendance_rate = round((present_count / total_records) * 100, 1)
    
    context = {
        'page_title': f'Session: {session.session_name}',
        'session': session,
        'attendance_records': attendance_records,
        'total_records': total_records,
        'present_count': present_count,
        'apology_count': apology_count,
        'absent_count': absent_count,
        'attendance_rate': attendance_rate,
    }
    return render(request, 'attendance/session_detail.html', context)


@login_required
def session_edit(request, session_id):
    """
    Edit an existing attendance session.
    Cannot edit if session is locked.
    """
    session = get_object_or_404(AttendanceSession, id=session_id)
    
    # Check if session is locked
    if session.is_locked:
        messages.warning(request, 'This session is locked and cannot be edited.')
        return redirect('attendance:session_detail', session_id=session.id)
    
    if request.method == 'POST':
        form = AttendanceSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, f'Session "{session.session_name}" updated successfully!')
            return redirect('attendance:session_detail', session_id=session.id)
    else:
        form = AttendanceSessionForm(instance=session)
    
    context = {
        'page_title': f'Edit Session: {session.session_name}',
        'form': form,
        'session': session,
        'action': 'Update'
    }
    return render(request, 'attendance/session_form.html', context)


@login_required
def session_delete(request, session_id):
    """
    Soft delete a session (mark as inactive).
    POST request required for security.
    """
    if request.method == 'POST':
        session = get_object_or_404(AttendanceSession, id=session_id)
        
        # Check if session is locked
        if session.is_locked:
            messages.warning(request, 'Cannot delete a locked session.')
            return redirect('attendance:session_detail', session_id=session.id)
        
        session.is_active = False
        session.save()
        messages.success(request, f'Session "{session.session_name}" removed.')
        return redirect('attendance:session_list')
    
    return redirect('attendance:session_detail', session_id=session_id)


@login_required
def mark_attendance(request, session_id):
    """
    Mark attendance for a session (bulk or individual).
    Shows all relevant members based on session hierarchy.
    Mobile-responsive with quick toggle buttons.
    """
    session = get_object_or_404(AttendanceSession, id=session_id)
    
    # Check if session is locked
    if session.is_locked:
        messages.warning(request, 'This session is locked. Attendance cannot be marked.')
        return redirect('attendance:session_detail', session_id=session.id)
    
    # Get relevant members based on session hierarchy
    if session.church:
        members = Member.objects.filter(user_home_church=session.church, is_active=True)
    elif session.pastorate:
        members = Member.objects.filter(
            user_home_church__pastorate=session.pastorate,
            is_active=True
        )
    elif session.diocese:
        members = Member.objects.filter(
            user_home_church__pastorate__diocese=session.diocese,
            is_active=True
        )
    elif session.is_dean_session:
        members = Member.objects.filter(is_active=True)
    else:
        members = Member.objects.none()
    
    members = members.order_by('last_name', 'first_name')
    
    # Get existing attendance records
    existing_records = {
        record.member_id: record 
        for record in session.attendance_records.select_related('member')
    }
    
    if request.method == 'POST':
        # Handle bulk attendance marking
        action = request.POST.get('action')
        
        if action == 'bulk_mark':
            # Bulk mark selected members
            member_ids = request.POST.getlist('member_ids')
            status = request.POST.get('bulk_status', 'present')
            
            if member_ids:
                count = bulk_mark_attendance(
                    session=session,
                    member_ids=member_ids,
                    status=status,
                    marked_by=request.user
                )
                messages.success(request, f'Attendance marked for {count} members as {status}.')
            else:
                messages.warning(request, 'Please select at least one member.')
        
        elif action == 'individual_mark':
            # Mark individual member
            member_id = request.POST.get('member_id')
            status = request.POST.get('status')
            
            if member_id and status:
                member = get_object_or_404(Member, id=member_id)
                record, created = AttendanceRecord.objects.update_or_create(
                    session=session,
                    member=member,
                    defaults={
                        'status': status,
                        'marked_by': request.user
                    }
                )
                messages.success(request, f'Attendance marked for {member.full_name} as {status}.')
                
                # Update session statistics
                session.update_statistics()
        
        return redirect('attendance:mark_attendance', session_id=session.id)
    
    # Prepare members with their attendance status
    members_with_status = []
    for member in members:
        record = existing_records.get(member.id)
        members_with_status.append({
            'member': member,
            'record': record,
            'status': record.status if record else None
        })
    
    # Pagination (50 members per page for bulk marking)
    paginator = Paginator(members_with_status, 50)
    page_number = request.GET.get('page')
    members_page = paginator.get_page(page_number)
    
    context = {
        'page_title': f'Mark Attendance: {session.session_name}',
        'session': session,
        'members_page': members_page,
        'total_members': members.count(),
        'total_marked': len(existing_records),
    }
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
def edit_attendance_record(request, record_id):
    """
    Edit an individual attendance record.
    Allows changing status, adding notes, etc.
    """
    record = get_object_or_404(
        AttendanceRecord.objects.select_related('session', 'member'),
        id=record_id
    )
    
    # Check if session is locked
    if record.session.is_locked:
        messages.warning(request, 'Cannot edit attendance for a locked session.')
        return redirect('attendance:session_detail', session_id=record.session.id)
    
    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            updated_record = form.save(commit=False)
            updated_record.marked_by = request.user
            updated_record.save()
            
            # Update session statistics
            record.session.update_statistics()
            
            messages.success(request, f'Attendance record updated for {record.member.full_name}.')
            return redirect('attendance:session_detail', session_id=record.session.id)
    else:
        form = AttendanceRecordForm(instance=record)
    
    context = {
        'page_title': f'Edit Attendance: {record.member.full_name}',
        'form': form,
        'record': record,
    }
    return render(request, 'attendance/edit_attendance_record.html', context)


@login_required
def attendance_statistics(request):
    """
    Display attendance statistics dashboard.
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
    
    # Calculate statistics directly
    sessions = AttendanceSession.objects.filter(
        session_date__range=[start_date, end_date]
    )
    
    # Filter by hierarchy level
    if church:
        sessions = sessions.filter(church=church)
    elif pastorate:
        sessions = sessions.filter(church__pastorate=pastorate)
    elif diocese:
        sessions = sessions.filter(church__pastorate__diocese=diocese)
    
    # Calculate summary stats
    total_sessions = sessions.count()
    sessions_this_month = sessions.filter(
        session_date__year=timezone.now().year,
        session_date__month=timezone.now().month
    ).count()
    
    # Calculate overall average attendance
    total_records = AttendanceRecord.objects.filter(session__in=sessions).count()
    present_records = AttendanceRecord.objects.filter(
        session__in=sessions, status='present'
    ).count()
    overall_average = (present_records / total_records * 100) if total_records > 0 else 0
    
    # Group by session type
    by_session_type = sessions.values('session_type').annotate(
        count=Count('id'),
        avg_percentage=Avg('attendance_percentage')
    ).order_by('-count')
    
    # Group by church
    by_church = sessions.values('church__name').annotate(
        count=Count('id'),
        avg_percentage=Avg('attendance_percentage')
    ).order_by('-count')[:10]
    
    # Get recent sessions
    recent_sessions = sessions.order_by('-session_date')[:15]
    
    # Get hierarchy options for filters
    churches = Church.objects.all().order_by('name')
    pastorates = Pastorate.objects.all().order_by('name')
    dioceses = Diocese.objects.all().order_by('name')
    
    context = {
        'page_title': 'Attendance Statistics',
        'total_sessions': total_sessions,
        'sessions_this_month': sessions_this_month,
        'overall_average': overall_average,
        'total_records': total_records,
        'by_session_type': by_session_type,
        'by_church': by_church,
        'recent_sessions': recent_sessions,
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
    return render(request, 'attendance/statistics.html', context)


@login_required
def absence_tracking(request):
    """
    View members with high absence streaks.
    Shows members who need follow-up (3+ consecutive absences).
    Mobile-responsive list with contact options.
    """
    # Get filter parameters
    church_id = request.GET.get('church')
    min_streak = int(request.GET.get('min_streak', 1))
    
    # Get all absence streaks
    all_streaks = AbsenceStreak.objects.select_related(
        'member', 'church'
    ).filter(current_streak__gte=min_streak).order_by('-current_streak')
    
    # Filter by church if specified
    if church_id:
        all_streaks = all_streaks.filter(church_id=church_id)
    
    # Calculate alert counts
    critical_count = all_streaks.filter(current_streak__gte=3).count()
    warning_count = all_streaks.filter(current_streak=2).count()
    total_monitored = Member.objects.filter(is_active=True).count()
    
    # Prepare absence alerts with additional data
    absence_alerts = []
    for streak in all_streaks:
        # Get last session where member was present
        last_present_record = AttendanceRecord.objects.filter(
            member=streak.member,
            status='present'
        ).select_related('session').order_by('-session__session_date').first()
        
        absence_alerts.append({
            'member': streak.member,
            'consecutive_count': streak.current_streak,
            'last_present_session': last_present_record.session if last_present_record else None,
        })
    
    # Pagination
    paginator = Paginator(absence_alerts, 25)
    page_number = request.GET.get('page')
    alerts_page = paginator.get_page(page_number)
    
    # Get churches for filter
    churches = Church.objects.all().order_by('name')
    
    context = {
        'page_title': 'Absence Tracking',
        'absence_alerts': alerts_page,
        'churches': churches,
        'min_streak': min_streak,
        'critical_count': critical_count,
        'warning_count': warning_count,
        'total_monitored': total_monitored,
    }
    return render(request, 'attendance/absence_tracking.html', context)


@login_required
def lock_session(request, session_id):
    """
    Lock a session to prevent further changes.
    POST request required.
    """
    if request.method == 'POST':
        session = get_object_or_404(AttendanceSession, id=session_id)
        session.is_locked = True
        session.save()
        messages.success(request, f'Session "{session.session_name}" is now locked.')
        return redirect('attendance:session_detail', session_id=session.id)
    
    return redirect('attendance:session_list')


@login_required
def unlock_session(request, session_id):
    """
    Unlock a session to allow changes.
    POST request required. Requires staff permission.
    """
    if not request.user.is_staff:
        messages.error(request, 'Only staff members can unlock sessions.')
        return redirect('attendance:session_detail', session_id=session_id)
    
    if request.method == 'POST':
        session = get_object_or_404(AttendanceSession, id=session_id)
        session.is_locked = False
        session.save()
        messages.success(request, f'Session "{session.session_name}" is now unlocked.')
        return redirect('attendance:session_detail', session_id=session.id)
    
    return redirect('attendance:session_list')
