
from django.shortcuts import render

def index(request):
    """Visitors main view"""
    context = {
        'page_title': 'Visitors Management'
    }
    return render(request, 'visitors/index.html', context)
