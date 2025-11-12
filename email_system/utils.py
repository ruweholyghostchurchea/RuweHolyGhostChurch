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


def send_html_email(subject, html_content, recipient_email, recipient_name, campaign=None, context=None, attachments=None):
    """
    Send a single HTML email with church branding
    
    Args:
        subject: Email subject line
        html_content: HTML content (will be wrapped in base template)
        recipient_email: Recipient email address
        recipient_name: Recipient full name
        campaign: EmailCampaign instance (optional)
        context: Additional context data for template (optional)
        attachments: List of EmailCampaignAttachment instances (optional)
    
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
        
        # Add attachments
        if attachments:
            for attachment in attachments:
                try:
                    email.attach_file(attachment.file.path, mimetype=attachment.content_type)
                except Exception as e:
                    logger.warning(f"Failed to attach file {attachment.filename}: {str(e)}")
        
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


def send_member_update_email(member):
    """
    Send email notification when member details are updated
    
    Args:
        member: Member instance
    """
    if not member.email_address:
        logger.warning(f"Cannot send update email to {member.full_name}: No email address")
        return None
    
    context = {
        'member': member,
        'login_link': f"{get_email_base_context()['site_url']}/auth/login/",
        'member_portal_link': f"{get_email_base_context()['site_url']}/members/",
    }
    
    # Create email content
    html_content = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #dc2626;">Member Profile Updated</h2>
        <p>Dear {member.full_name},</p>
        <p>This is to inform you that your member profile has been updated in our church system.</p>
        <p>If you did not make these changes or have any concerns, please contact the church administration immediately.</p>
        <p>You can view your updated profile by logging into the member portal:</p>
        <p style="margin: 20px 0;">
            <a href="{context['member_portal_link']}" style="background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                View My Profile
            </a>
        </p>
        <p>God bless you!</p>
    </div>
    """
    
    subject = "Your Member Profile Has Been Updated"
    
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
    # Get campaign attachments
    attachments = list(campaign.attachments.all())
    
    sent_count = 0
    failed_count = 0
    
    # Get member recipients
    if campaign.recipient_type == 'custom_emails':
        # Send to custom email addresses
        total_recipients = len(campaign.custom_emails)
        campaign.total_recipients = total_recipients
        campaign.status = 'sending'
        campaign.save()
        
        for email_address in campaign.custom_emails:
            email_log = send_html_email(
                subject=campaign.subject,
                html_content=campaign.html_content,
                recipient_email=email_address,
                recipient_name=email_address.split('@')[0],
                campaign=campaign,
                context={},
                attachments=attachments
            )
            
            if email_log.status == 'sent':
                sent_count += 1
            else:
                failed_count += 1
    else:
        # Send to members
        members = get_campaign_recipients(campaign)
        total_recipients = members.count()
        
        campaign.total_recipients = total_recipients
        campaign.status = 'sending'
        campaign.save()
        
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
                context=context,
                attachments=attachments
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
        'total': campaign.total_recipients
    }
