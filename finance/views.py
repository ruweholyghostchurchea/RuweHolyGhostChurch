from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Finance main view"""
    context = {
        'page_title': 'Financial Management'
    }
    return render(request, 'finance/index.html', context)