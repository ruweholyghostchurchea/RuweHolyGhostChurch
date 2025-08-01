from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Church settings main view"""
    context = {
        'page_title': 'Church Settings'
    }
    return render(request, 'church_settings/index.html', context)