from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Reports main view"""
    context = {
        'page_title': 'Reports & Analytics'
    }
    return render(request, 'reports/index.html', context)