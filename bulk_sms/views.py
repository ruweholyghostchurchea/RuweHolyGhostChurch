
from django.shortcuts import render

def index(request):
    """Bulk SMS main view"""
    context = {
        'page_title': 'Bulk SMS Management'
    }
    return render(request, 'bulk_sms/index.html', context)
