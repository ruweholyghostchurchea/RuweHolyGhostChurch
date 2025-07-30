
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta

def index(request):
    """Dashboard main view with statistics"""
    
    # Mock data - replace with actual model queries once models are created
    context = {
        'total_members': 150,
        'total_visitors': 25,
        'this_week_attendance': 120,
        'monthly_offering': 15000,
        'recent_activities': [
            {
                'icon': 'fas fa-user-plus',
                'activity': 'New member registered: John Doe',
                'time': '2 hours ago',
                'color': 'success'
            },
            {
                'icon': 'fas fa-dollar-sign', 
                'activity': 'Offering received: $500',
                'time': '5 hours ago',
                'color': 'primary'
            },
            {
                'icon': 'fas fa-calendar-check',
                'activity': 'Sunday service attendance: 85 members',
                'time': '1 day ago',
                'color': 'info'
            },
            {
                'icon': 'fas fa-sms',
                'activity': 'Bulk SMS sent to 100 members',
                'time': '2 days ago',
                'color': 'warning'
            }
        ],
        'upcoming_events': [
            {
                'title': 'Sunday Service',
                'date': 'Dec 24, 2024',
                'time': '9:00 AM',
                'location': 'Main Sanctuary'
            },
            {
                'title': 'Bible Study',
                'date': 'Dec 26, 2024', 
                'time': '7:00 PM',
                'location': 'Fellowship Hall'
            },
            {
                'title': 'Youth Meeting',
                'date': 'Dec 28, 2024',
                'time': '6:00 PM', 
                'location': 'Youth Center'
            }
        ]
    }
    
    return render(request, 'dashboard/index.html', context)
