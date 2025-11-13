from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseForbidden
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import EmailCampaign, EmailLog, EmailTemplate, EmailCampaignAttachment
from members.models import Member
from church_structure.models import Diocese, Pastorate, Church
from .utils import send_campaign_emails, get_campaign_recipients
from datetime import datetime
import mimetypes


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
            
            # Parse custom email addresses
            custom_emails = []
            if recipient_type == 'custom_emails':
                custom_emails_raw = request.POST.get('custom_emails', '')
                emails_list = [email.strip() for email in custom_emails_raw.split(',') if email.strip()]
                
                for email in emails_list:
                    try:
                        validate_email(email)
                        custom_emails.append(email)
                    except ValidationError:
                        messages.warning(request, f'Invalid email address skipped: {email}')
                
                if not custom_emails:
                    messages.error(request, 'No valid email addresses provided for custom recipients.')
                    return redirect('email_system:compose')
            
            # Create campaign
            campaign = EmailCampaign.objects.create(
                name=name,
                subject=subject,
                html_content=html_content,
                recipient_type=recipient_type,
                recipient_filter=recipient_filter,
                custom_emails=custom_emails,
                status='draft',
                created_by=request.user
            )
            
            # Handle file attachments with validation
            uploaded_files = request.FILES.getlist('attachments')
            MAX_FILE_SIZE = 10 * 1024 * 1024
            ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.txt', '.xlsx', '.xls']
            ALLOWED_MIME_TYPES = [
                'application/pdf', 'application/msword', 
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'image/jpeg', 'image/png', 'image/gif', 'text/plain',
                'application/vnd.ms-excel', 
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ]
            
            for uploaded_file in uploaded_files:
                import os
                file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                
                if uploaded_file.size > MAX_FILE_SIZE:
                    messages.warning(request, f'File {uploaded_file.name} is too large (max 10MB). Skipped.')
                    continue
                
                if file_ext not in ALLOWED_EXTENSIONS:
                    messages.warning(request, f'File type {file_ext} not allowed for {uploaded_file.name}. Skipped.')
                    continue
                
                content_type, _ = mimetypes.guess_type(uploaded_file.name)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                if content_type not in ALLOWED_MIME_TYPES and content_type != 'application/octet-stream':
                    messages.warning(request, f'MIME type not allowed for {uploaded_file.name}. Skipped.')
                    continue
                
                EmailCampaignAttachment.objects.create(
                    campaign=campaign,
                    file=uploaded_file,
                    filename=uploaded_file.name,
                    file_size=uploaded_file.size,
                    content_type=content_type
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


@staff_required
def resend_failed_email(request, log_id):
    """Resend a failed email"""
    from .utils import send_html_email
    
    email_log = get_object_or_404(EmailLog, id=log_id)
    
    # Only allow resending failed or bounced emails
    if email_log.status not in ['failed', 'bounced']:
        messages.error(request, 'Only failed or bounced emails can be resent.')
        return redirect('email_system:logs')
    
    try:
        # Get campaign attachments if this was part of a campaign
        attachments = []
        if email_log.campaign:
            attachments = list(email_log.campaign.attachments.all())
        
        # Resend the email using the same content
        new_log = send_html_email(
            subject=email_log.subject,
            html_content=email_log.html_content,
            recipient_email=email_log.recipient_email,
            recipient_name=email_log.recipient_name,
            campaign=email_log.campaign,
            context={},
            attachments=attachments
        )
        
        if new_log.status == 'sent':
            # Update campaign counts if this was part of a campaign
            if email_log.campaign:
                campaign = email_log.campaign
                campaign.sent_count += 1
                campaign.failed_count = max(0, campaign.failed_count - 1)
                campaign.save()
            
            messages.success(request, f'Email successfully resent to {email_log.recipient_email}')
        else:
            messages.error(request, f'Failed to resend email: {new_log.error_message}')
    
    except Exception as e:
        messages.error(request, f'Error resending email: {str(e)}')
    
    return redirect('email_system:logs')
