"""
Email utility functions for sending emails to members
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from members.models import Member
from church_structure.models import Diocese, Pastorate, Church
from .models import EmailLog, EmailCampaign
import logging

logger = logging.getLogger(__name__)


def get_email_base_context():
    """Get base context data for all emails"""
    return {
        'site_name': 'Ruwe Holy Ghost Church of East Africa',
        'site_url': 'https://ruweholyghostchurch.org',
        'logo_url': 'https://i.imgur.com/8ToqmB8.png',
        'contact_email': 'info@ruweholyghostchurch.org',
        'phone': '+254713049858',
        'current_year': timezone.now().year,
    }


def send_html_email(subject, html_content, recipient_email, recipient_name, campaign=None, context=None):
    """
    Send a single HTML email with church branding
    
    Args:
        subject: Email subject line
        html_content: HTML content (will be wrapped in base template)
        recipient_email: Recipient email address
        recipient_name: Recipient full name
        campaign: EmailCampaign instance (optional)
        context: Additional context data for template (optional)
    
    Returns:
        EmailLog instance
    """
    # Create email log
    email_log = EmailLog.objects.create(
        campaign=campaign,
        recipient_email=recipient_email,
        recipient_name=recipient_name,
        subject=subject,
        html_content=html_content,
        status='pending'
    )
    
    try:
        # Prepare context
        email_context = get_email_base_context()
        email_context.update({
            'recipient_name': recipient_name,
            'content': html_content,
        })
        if context:
            email_context.update(context)
        
        # Render email with base template
        html_message = render_to_string('email_system/emails/base.html', email_context)
        text_message = strip_tags(html_message)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
            reply_to=settings.EMAIL_REPLY_TO
        )
        email.attach_alternative(html_message, "text/html")
        
        # Send email
        email.send(fail_silently=False)
        
        # Update log
        email_log.status = 'sent'
        email_log.sent_at = timezone.now()
        email_log.save()
        
        logger.info(f"Email sent successfully to {recipient_email}: {subject}")
        return email_log
        
    except Exception as e:
        # Log error
        email_log.status = 'failed'
        email_log.error_message = str(e)
        email_log.save()
        
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
        return email_log


def send_welcome_email(member):
    """
    Send welcome email to newly registered member
    
    Args:
        member: Member instance
    """
    if not member.email_address:
        logger.warning(f"Cannot send welcome email to {member.full_name}: No email address")
        return None
    
    # Prepare password reset link
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    
    password_reset_link = ""
    if member.user:
        uid = urlsafe_base64_encode(force_bytes(member.user.pk))
        token = default_token_generator.make_token(member.user)
        password_reset_link = f"{get_email_base_context()['site_url']}/auth/forgot-password/"
    
    context = {
        'member': member,
        'password_reset_link': password_reset_link,
        'login_link': f"{get_email_base_context()['site_url']}/auth/login/",
        'member_portal_link': f"{get_email_base_context()['site_url']}/members/",
    }
    
    # Render welcome email template
    html_content = render_to_string('email_system/emails/welcome.html', context)
    
    subject = "Welcome to Ruwe Holy Ghost Church of East Africa"
    
    return send_html_email(
        subject=subject,
        html_content=html_content,
        recipient_email=member.email_address,
        recipient_name=member.full_name,
        context=context
    )


def get_campaign_recipients(campaign):
    """
    Get list of members based on campaign recipient type
    
    Args:
        campaign: EmailCampaign instance
    
    Returns:
        QuerySet of Member objects
    """
    # Start with active members who have email addresses
    members = Member.objects.filter(
        membership_status='Active',
        email_address__isnull=False
    ).exclude(email_address='')
    
    # Filter based on recipient type
    if campaign.recipient_type == 'youth':
        members = members.filter(user_group='Youth')
    elif campaign.recipient_type == 'adult':
        members = members.filter(user_group='Adult')
    elif campaign.recipient_type == 'elder':
        members = members.filter(user_group='Elder')
    elif campaign.recipient_type == 'clergy':
        members = members.filter(member_roles__contains=['clergy'])
    elif campaign.recipient_type == 'staff':
        members = members.filter(is_staff=True)
    elif campaign.recipient_type == 'ordained':
        members = members.filter(is_ordained=True)
    elif campaign.recipient_type == 'diocese':
        diocese_id = campaign.recipient_filter.get('diocese_id')
        if diocese_id:
            members = members.filter(user_home_diocese_id=diocese_id)
    elif campaign.recipient_type == 'pastorate':
        pastorate_id = campaign.recipient_filter.get('pastorate_id')
        if pastorate_id:
            members = members.filter(user_home_pastorate_id=pastorate_id)
    elif campaign.recipient_type == 'church':
        church_id = campaign.recipient_filter.get('church_id')
        if church_id:
            members = members.filter(user_home_church_id=church_id)
    
    return members


def send_campaign_emails(campaign):
    """
    Send emails for a campaign
    
    Args:
        campaign: EmailCampaign instance
    
    Returns:
        dict with sent_count and failed_count
    """
    # Get recipients
    members = get_campaign_recipients(campaign)
    
    # Update campaign
    campaign.total_recipients = members.count()
    campaign.status = 'sending'
    campaign.save()
    
    sent_count = 0
    failed_count = 0
    
    # Send emails to each member
    for member in members:
        context = {
            'member': member,
        }
        
        email_log = send_html_email(
            subject=campaign.subject,
            html_content=campaign.html_content,
            recipient_email=member.email_address,
            recipient_name=member.full_name,
            campaign=campaign,
            context=context
        )
        
        if email_log.status == 'sent':
            sent_count += 1
        else:
            failed_count += 1
    
    # Update campaign
    campaign.sent_count = sent_count
    campaign.failed_count = failed_count
    campaign.status = 'sent' if failed_count == 0 else 'failed'
    campaign.sent_at = timezone.now()
    campaign.save()
    
    logger.info(f"Campaign '{campaign.name}' sent: {sent_count} successful, {failed_count} failed")
    
    return {
        'sent_count': sent_count,
        'failed_count': failed_count,
        'total': members.count()
    }
