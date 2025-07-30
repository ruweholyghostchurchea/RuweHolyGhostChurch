from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    """Church settings main view"""
    context = {
        'page_title': 'Church Settings'
    }
    return render(request, 'church_settings/index.html', context)
