"""
Utility functions for the Visitors app.
Includes email notifications and helper functions.
"""

from django.template.loader import render_to_string
from email_system.utils import send_html_email
import logging

logger = logging.getLogger(__name__)


def send_first_visit_email(visitor):
    """
    Send welcome/thank you email to visitor after their first visit.
    
    Args:
        visitor: Visitor instance
        
    Returns:
        EmailLog instance or None
    """
    if not visitor.email_address:
        logger.warning(f"Cannot send first visit email to {visitor.full_name}: No email address")
        return None
    
    # Prepare email content
    context = {
        'visitor': visitor,
        'church_name': visitor.church.name if visitor.church else 'Ruwe Holy Ghost Church EA',
    }
    
    # Create HTML content
    html_content = f"""
    <h2>Welcome to {context['church_name']}!</h2>
    <p>Dear {visitor.full_name},</p>
    
    <p>Thank you for visiting us on {visitor.first_visit_date.strftime('%B %d, %Y')}. 
    We are blessed to have had you with us during our worship service.</p>
    
    <p>At Ruwe Holy Ghost Church of East Africa, we believe in the power of the Holy Spirit 
    and strive to create a community where everyone can experience God's love and presence.</p>
    
    <h3>We'd Love to Stay Connected</h3>
    <p>If you have any questions or would like to learn more about our church, please don't 
    hesitate to reach out. We'd love to hear from you!</p>
    
    <p>We hope to see you again soon!</p>
    
    <p><strong>Service Times:</strong><br>
    Saturday Sabbath Services: 6:00 AM, 9:00 AM, 12:00 PM, 3:00 PM</p>
    
    <p>God bless you,<br>
    <strong>Ruwe Holy Ghost Church EA</strong></p>
    """
    
    subject = f"Thank You for Visiting {context['church_name']}"
    
    return send_html_email(
        subject=subject,
        html_content=html_content,
        recipient_email=visitor.email_address,
        recipient_name=visitor.full_name,
        context=context
    )


def send_subsequent_visit_email(visitor, visit):
    """
    Send thank you email for subsequent visits (2nd, 3rd, etc.).
    
    Args:
        visitor: Visitor instance
        visit: VisitorVisit instance
        
    Returns:
        EmailLog instance or None
    """
    if not visitor.email_address:
        logger.warning(f"Cannot send visit email to {visitor.full_name}: No email address")
        return None
    
    # Prepare email content
    context = {
        'visitor': visitor,
        'visit': visit,
        'church_name': visitor.church.name if visitor.church else 'Ruwe Holy Ghost Church EA',
    }
    
    # Create HTML content
    html_content = f"""
    <h2>Welcome Back to {context['church_name']}!</h2>
    <p>Dear {visitor.full_name},</p>
    
    <p>It's wonderful to see you again! Thank you for your {visit.visit_number}
    {"nd" if visit.visit_number == 2 else "rd" if visit.visit_number == 3 else "th"} 
    visit on {visit.visit_date.strftime('%B %d, %Y')}.</p>
    
    <p>We're so glad you're continuing to worship with us. Your presence enriches our 
    community, and we hope you're finding a spiritual home with us.</p>
    
    {"<p>We noticed you've expressed interest in becoming a member. We'd love to talk with you about membership! Please feel free to reach out to us.</p>" if visitor.interested_in_membership else ""}
    
    <p>We look forward to seeing you again soon!</p>
    
    <p>God bless you,<br>
    <strong>Ruwe Holy Ghost Church EA</strong></p>
    """
    
    subject = f"Thank You for Visiting Again - {context['church_name']}"
    
    # Try to send email with proper error handling
    try:
        # Send email
        email_log = send_html_email(
            subject=subject,
            html_content=html_content,
            recipient_email=visitor.email_address,
            recipient_name=visitor.full_name,
            context=context
        )
        
        # Mark email as sent only if successful
        if email_log and email_log.status == 'sent':
            visit.email_sent = True
            visit.save()
            logger.info(f"Subsequent visit email sent successfully to {visitor.full_name}")
        else:
            logger.warning(f"Email to {visitor.full_name} was created but not sent successfully")
        
        return email_log
        
    except Exception as e:
        # If email sending fails due to exception, log it and don't mark as sent
        logger.error(f"Failed to send subsequent visit email to {visitor.full_name}: {str(e)}")
        visit.email_sent = False
        visit.save()
        return None


def calculate_visitor_statistics(level='church', church=None, pastorate=None, diocese=None, start_date=None, end_date=None):
    """
    Calculate visitor statistics for a given hierarchy level and date range.
    
    Args:
        level: Hierarchy level ('church', 'pastorate', 'diocese', 'dean')
        church: Church instance (for church level)
        pastorate: Pastorate instance (for pastorate level)
        diocese: Diocese instance (for diocese level)
        start_date: Start date for statistics
        end_date: End date for statistics
        
    Returns:
        Dictionary with statistics
    """
    from .models import Visitor
    from django.db.models import Count, Q
    
    # Build query based on level
    query = Q()
    
    if level == 'church' and church:
        query = Q(church=church)
    elif level == 'pastorate' and pastorate:
        query = Q(pastorate=pastorate)
    elif level == 'diocese' and diocese:
        query = Q(diocese=diocese)
    elif level == 'dean':
        query = Q(is_dean_visitor=True)
    
    # Add date filter
    if start_date:
        query &= Q(first_visit_date__gte=start_date)
    if end_date:
        query &= Q(first_visit_date__lte=end_date)
    
    # Get visitors
    visitors = Visitor.objects.filter(query)
    
    # Calculate statistics
    stats = {
        'total_visitors': visitors.count(),
        'first_time_visitors': visitors.filter(visits__isnull=True).count() or visitors.count(),
        'return_visitors': visitors.exclude(visits__isnull=True).count(),
        'converted_to_members': visitors.filter(converted_to_member=True).count(),
        'male_count': visitors.filter(gender='M').count(),
        'female_count': visitors.filter(gender='F').count(),
        'youth_count': visitors.filter(age_group='youth').count(),
        'adult_count': visitors.filter(age_group='adult').count(),
        'elder_count': visitors.filter(age_group='elder').count(),
        'interested_in_membership': visitors.filter(interested_in_membership=True).count(),
    }
    
    return stats
