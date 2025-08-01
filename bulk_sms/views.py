from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Bulk SMS main view"""
    context = {
        'page_title': 'Bulk SMS Management'
    }
    return render(request, 'bulk_sms/index.html', context)