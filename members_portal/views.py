from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def dashboard(request):
    """
    Member dashboard - shows member's personal information and overview
    """
    # TODO: Implement member dashboard
    return HttpResponse('''
        <html>
        <head><title>Members Portal - Dashboard</title></head>
        <body>
            <h1>Welcome to Ruwe Holy Ghost Church Members Portal</h1>
            <p>Dashboard is under development.</p>
            <p>Logged in as: {}</p>
            <a href="/auth/logout/">Logout</a>
        </body>
        </html>
    '''.format(request.user.username))


@login_required
def profile(request):
    """
    Member profile view - allows member to view/edit their information
    """
    # TODO: Implement member profile
    return HttpResponse('<h1>Member Profile (Coming Soon)</h1>')


@login_required
def attendance(request):
    """
    Member attendance history view
    """
    # TODO: Implement attendance history
    return HttpResponse('<h1>My Attendance (Coming Soon)</h1>')


@login_required
def giving(request):
    """
    Member giving/contribution history view
    """
    # TODO: Implement giving history
    return HttpResponse('<h1>My Contributions (Coming Soon)</h1>')
