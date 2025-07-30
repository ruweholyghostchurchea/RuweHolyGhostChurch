
from django.shortcuts import render

def index(request):
    """Finance main view"""
    context = {
        'page_title': 'Financial Management'
    }
    return render(request, 'finance/index.html', context)
