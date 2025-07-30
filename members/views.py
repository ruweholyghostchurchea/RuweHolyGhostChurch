
from django.shortcuts import render

def index(request):
    """Members main view"""
    context = {
        'page_title': 'Members Management'
    }
    return render(request, 'members/index.html', context)
