from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """
    Public website homepage
    """
    # TODO: Implement homepage with church information
    return HttpResponse('''
        <html>
        <head><title>Ruwe Holy Ghost Church</title></head>
        <body>
            <h1>Welcome to Ruwe Holy Ghost Church</h1>
            <p>Public website is under development.</p>
            <nav>
                <ul>
                    <li><a href="/about/">About Us</a></li>
                    <li><a href="/contact/">Contact</a></li>
                    <li><a href="/events/">Events</a></li>
                </ul>
            </nav>
        </body>
        </html>
    ''')


def about(request):
    """
    About us page
    """
    # TODO: Implement about page
    return HttpResponse('<h1>About Ruwe Holy Ghost Church (Coming Soon)</h1>')


def contact(request):
    """
    Contact us page
    """
    # TODO: Implement contact form
    return HttpResponse('<h1>Contact Us (Coming Soon)</h1>')


def events(request):
    """
    Church events page
    """
    # TODO: Implement events listing
    return HttpResponse('<h1>Church Events (Coming Soon)</h1>')
