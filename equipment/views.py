
from django.shortcuts import render

def index(request):
    """Equipment main view"""
    context = {
        'page_title': 'Equipment Management'
    }
    return render(request, 'equipment/index.html', context)
