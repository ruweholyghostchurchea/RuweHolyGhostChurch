
from django.shortcuts import render

def index(request):
    """Reports main view"""
    context = {
        'page_title': 'Reports & Analytics'
    }
    return render(request, 'reports/index.html', context)
