from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Attendance main view"""
    context = {
        'page_title': 'Attendance Management'
    }
    return render(request, 'attendance/index.html', context)