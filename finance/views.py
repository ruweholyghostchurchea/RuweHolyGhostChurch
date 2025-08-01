
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Finance main view"""
    context = {
        'page_title': 'Financial Management'
    }
    return render(request, 'finance/index.html', context)
