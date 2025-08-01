
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Visitors main view"""
    context = {
        'page_title': 'Visitors Management'
    }
    return render(request, 'visitors/index.html', context)
