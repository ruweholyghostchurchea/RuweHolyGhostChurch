from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Equipment main view"""
    context = {
        'page_title': 'Equipment Management'
    }
    return render(request, 'equipment/index.html', context)