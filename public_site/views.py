from django.shortcuts import render


def home(request):
    """
    Public website homepage
    """
    return render(request, 'public_site/home.html')


def about(request):
    """
    About us page
    """
    return render(request, 'public_site/about.html')


def history(request):
    """
    Our history page
    """
    return render(request, 'public_site/history.html')


def services(request):
    """
    Worship and services page
    """
    return render(request, 'public_site/services.html')


def contact(request):
    """
    Contact us page
    """
    return render(request, 'public_site/contact.html')


def events(request):
    """
    Church events and calendar page
    """
    return render(request, 'public_site/events_calendar.html')


def donation(request):
    """
    Donation page
    """
    return render(request, 'public_site/donation.html')
