
from django.shortcuts import render

def index(request):
    """Attendance main view"""
    context = {
        'page_title': 'Attendance Management'
    }
    return render(request, 'attendance/index.html', context)
