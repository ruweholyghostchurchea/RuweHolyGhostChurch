
from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from members.models import Member
from visitors.models import Visitor
from attendance.models import Attendance, Service
from finance.models import Offering

def index(request):
    """Dashboard main view with statistics"""
    
    # Calculate date ranges
    now = timezone.now()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_week_start = now - timedelta(days=now.weekday())
    
    # Get statistics
    total_members = Member.objects.filter(membership_status='active').count()
    total_visitors = Visitor.objects.filter(visit_date__gte=current_month_start.date()).count()
    
    # This week's attendance
    this_week_services = Service.objects.filter(date__gte=current_week_start.date())
    this_week_attendance = Attendance.objects.filter(
        service__in=this_week_services, 
        present=True
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
            'activity': f'Weekly offering: ${Offering.objects.filter(date__gte=current_week_start.date()).aggregate(total=Sum("amount"))["total"] or 0}',
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
            'activity': f'New visitors this week: {Visitor.objects.filter(visit_date__gte=current_week_start.date()).count()}',
            'time': '2 days ago',
            'color': 'warning'
        }
    ]
    
    # Upcoming events (can be moved to a separate Event model later)
    upcoming_events = [
        {
            'title': 'Sunday Morning Service',
            'date': 'Dec 29, 2024',
            'time': '9:00 AM',
            'location': 'Main Sanctuary'
        },
        {
            'title': 'Bible Study',
            'date': 'Jan 1, 2025', 
            'time': '7:00 PM',
            'location': 'Fellowship Hall'
        },
        {
            'title': 'Youth Meeting',
            'date': 'Jan 3, 2025',
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
