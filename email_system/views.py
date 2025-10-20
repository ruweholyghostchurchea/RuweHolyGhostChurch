from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseForbidden
from .models import EmailCampaign, EmailLog, EmailTemplate
from members.models import Member
from church_structure.models import Diocese, Pastorate, Church
from .utils import send_campaign_emails, get_campaign_recipients
from datetime import datetime


def staff_required(view_func):
    """Decorator to require staff status for email system access"""
    def check_staff(user):
        return user.is_staff or user.is_superuser
    
    decorated_view = user_passes_test(check_staff, login_url='/dashboard/')(view_func)
    return login_required(decorated_view)


@staff_required
def index(request):
    """Email System dashboard"""
    # Statistics
    total_campaigns = EmailCampaign.objects.count()
    sent_campaigns = EmailCampaign.objects.filter(status='sent').count()
    draft_campaigns = EmailCampaign.objects.filter(status='draft').count()
    
    total_emails_sent = EmailLog.objects.filter(status='sent').count()
    failed_emails = EmailLog.objects.filter(status='failed').count()
    
    # Recent campaigns
    recent_campaigns = EmailCampaign.objects.all()[:10]
    
    # Recent email logs
    recent_logs = EmailLog.objects.all()[:20]
    
    context = {
        'page_title': 'Email System',
        'total_campaigns': total_campaigns,
        'sent_campaigns': sent_campaigns,
        'draft_campaigns': draft_campaigns,
        'total_emails_sent': total_emails_sent,
        'failed_emails': failed_emails,
        'recent_campaigns': recent_campaigns,
        'recent_logs': recent_logs,
    }
    return render(request, 'email_system/index.html', context)


@staff_required
def compose(request):
    """Compose and send email"""
    if request.method == 'GET':
        dioceses = Diocese.objects.filter(is_active=True).order_by('name')
        pastorates = Pastorate.objects.filter(is_active=True).order_by('name')
        churches = Church.objects.filter(is_active=True).order_by('name')
        templates = EmailTemplate.objects.filter(is_active=True)
        
        context = {
            'page_title': 'Compose Email',
            'dioceses': dioceses,
            'pastorates': pastorates,
            'churches': churches,
            'templates': templates,
            'recipient_types': EmailCampaign.RECIPIENT_TYPE_CHOICES,
        }
        return render(request, 'email_system/compose.html', context)
    
    elif request.method == 'POST':
        try:
            name = request.POST.get('name')
            subject = request.POST.get('subject')
            html_content = request.POST.get('html_content')
            recipient_type = request.POST.get('recipient_type')
            send_now = request.POST.get('send_now') == 'on'
            
            # Build recipient filter
            recipient_filter = {}
            if recipient_type == 'diocese':
                recipient_filter['diocese_id'] = request.POST.get('diocese_id')
            elif recipient_type == 'pastorate':
                recipient_filter['pastorate_id'] = request.POST.get('pastorate_id')
            elif recipient_type == 'church':
                recipient_filter['church_id'] = request.POST.get('church_id')
            
            # Create campaign
            campaign = EmailCampaign.objects.create(
                name=name,
                subject=subject,
                html_content=html_content,
                recipient_type=recipient_type,
                recipient_filter=recipient_filter,
                status='draft',
                created_by=request.user
            )
            
            if send_now:
                # Send immediately
                result = send_campaign_emails(campaign)
                messages.success(request, f'Email campaign sent successfully! {result["sent_count"]} sent, {result["failed_count"]} failed.')
                return redirect('email_system:campaign_detail', campaign_id=campaign.id)
            else:
                messages.success(request, f'Email campaign "{name}" saved as draft.')
                return redirect('email_system:campaigns')
        
        except Exception as e:
            messages.error(request, f'Error creating campaign: {str(e)}')
            return redirect('email_system:compose')


@staff_required
def campaigns(request):
    """View all email campaigns"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    campaigns_list = EmailCampaign.objects.all()
    
    if search_query:
        campaigns_list = campaigns_list.filter(
            Q(name__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    if status_filter:
        campaigns_list = campaigns_list.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(campaigns_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Email Campaigns',
        'campaigns': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': EmailCampaign.STATUS_CHOICES,
    }
    return render(request, 'email_system/campaigns.html', context)


@staff_required
def campaign_detail(request, campaign_id):
    """View campaign details"""
    campaign = get_object_or_404(EmailCampaign, id=campaign_id)
    
    # Get email logs for this campaign
    email_logs = EmailLog.objects.filter(campaign=campaign)
    
    context = {
        'page_title': f'Campaign: {campaign.name}',
        'campaign': campaign,
        'email_logs': email_logs,
    }
    return render(request, 'email_system/campaign_detail.html', context)


@staff_required
def send_campaign(request, campaign_id):
    """Send a draft campaign"""
    campaign = get_object_or_404(EmailCampaign, id=campaign_id)
    
    if campaign.status != 'draft':
        messages.error(request, 'Only draft campaigns can be sent.')
        return redirect('email_system:campaign_detail', campaign_id=campaign.id)
    
    try:
        result = send_campaign_emails(campaign)
        messages.success(request, f'Campaign sent! {result["sent_count"]} sent, {result["failed_count"]} failed.')
    except Exception as e:
        messages.error(request, f'Error sending campaign: {str(e)}')
    
    return redirect('email_system:campaign_detail', campaign_id=campaign.id)


@staff_required
def email_logs(request):
    """View all email logs"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    logs_list = EmailLog.objects.all().select_related('campaign', 'recipient')
    
    if search_query:
        logs_list = logs_list.filter(
            Q(recipient_email__icontains=search_query) |
            Q(recipient_name__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    if status_filter:
        logs_list = logs_list.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(logs_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Email Logs',
        'logs': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': EmailLog.STATUS_CHOICES,
    }
    return render(request, 'email_system/logs.html', context)


@staff_required
def preview_recipients(request):
    """Preview recipients for a campaign (AJAX)"""
    recipient_type = request.GET.get('recipient_type')
    diocese_id = request.GET.get('diocese_id')
    pastorate_id = request.GET.get('pastorate_id')
    church_id = request.GET.get('church_id')
    
    # Create temporary campaign object
    campaign = EmailCampaign(
        recipient_type=recipient_type,
        recipient_filter={
            'diocese_id': diocese_id,
            'pastorate_id': pastorate_id,
            'church_id': church_id,
        }
    )
    
    recipients = get_campaign_recipients(campaign)
    
    return JsonResponse({
        'count': recipients.count(),
        'recipients': [
            {
                'name': m.full_name,
                'email': m.email_address,
                'church': m.user_home_church.name if m.user_home_church else 'N/A'
            }
            for m in recipients[:50]  # Limit preview to 50
        ]
    })
