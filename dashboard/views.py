from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from members.models import Member
from visitors.models import Visitor
from attendance.models import AttendanceRecord, AttendanceSession
from finance.models import Offering

@login_required
def index(request):
    """Dashboard main view with statistics"""

    # Calculate date ranges
    now = timezone.now()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_week_start = now - timedelta(days=now.weekday())

    # Get statistics
    total_members = Member.objects.filter(membership_status='Active').count()
    total_visitors = Visitor.objects.filter(first_visit_date__gte=current_month_start.date()).count()

    # This week's attendance
    this_week_sessions = AttendanceSession.objects.filter(session_date__gte=current_week_start.date())
    this_week_attendance = AttendanceRecord.objects.filter(
        session__in=this_week_sessions, 
        status='present'
    ).count()

    # Monthly offering
    monthly_offering = Offering.objects.filter(
        date__gte=current_month_start.date()
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Recent activities (mock data for now - can be replaced with actual activity log)
    recent_activities = [
        {
            'icon': 'fas fa-user-plus',
            'activity': f'New members registered: {Member.objects.filter(created_at__gte=now - timedelta(days=7)).count()}',
            'time': '2 hours ago',
            'color': 'success'
        },
        {
            'icon': 'fas fa-dollar-sign', 
            'activity': f'Weekly Tithe/Offering: KShs. {Offering.objects.filter(date__gte=current_week_start.date()).aggregate(total=Sum("amount"))["total"] or 0}',
            'time': '5 hours ago',
            'color': 'primary'
        },
        {
            'icon': 'fas fa-calendar-check',
            'activity': f'Recent service attendance: {this_week_attendance} members',
            'time': '1 day ago',
            'color': 'info'
        },
        {
            'icon': 'fas fa-user-friends',
            'activity': f'New visitors this week: {Visitor.objects.filter(first_visit_date__gte=current_week_start.date()).count()}',
            'time': '2 days ago',
            'color': 'warning'
        }
    ]

    # Upcoming events (can be moved to a separate Event model later)
    upcoming_events = [
        {
            'title': 'Saturday Sabbath Service',
            'date': 'Aug 2, 2025',
            'time': '9:00 AM',
            'location': 'Main Church, Ruwe, Siaya County'
        },
        {
            'title': 'Bible Study',
            'date': 'Jan 18, 2026', 
            'time': '7:00 PM',
            'location': 'Fellowship Hall'
        },
        {
            'title': 'Youth Meeting',
            'date': 'Jan 19, 2026',
            'time': '6:00 PM', 
            'location': 'Youth Center'
        }
    ]

    context = {
        'total_members': total_members,
        'total_visitors': total_visitors,
        'this_week_attendance': this_week_attendance,
        'monthly_offering': monthly_offering,
        'recent_activities': recent_activities,
        'upcoming_events': upcoming_events,
    }

    return render(request, 'dashboard/index.html', context)