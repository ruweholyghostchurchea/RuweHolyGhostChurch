"""
Signals for the Visitors app.
Handles automatic email notifications and other automated tasks.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Visitor, VisitorVisit
from .utils import send_first_visit_email, send_subsequent_visit_email
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Visitor)
def send_visitor_welcome_email(sender, instance, created, **kwargs):
    """
    Send welcome email when a new visitor is created.
    Only sends if visitor has an email address.
    """
    if created and instance.email_address:
        try:
            send_first_visit_email(instance)
            logger.info(f"Welcome email sent to visitor: {instance.full_name}")
        except Exception as e:
            logger.error(f"Failed to send welcome email to {instance.full_name}: {str(e)}")


@receiver(post_save, sender=VisitorVisit)
def send_visitor_return_email(sender, instance, created, **kwargs):
    """
    Send thank you email when a visitor returns (subsequent visit).
    Only sends if visitor has email and email hasn't been sent already.
    """
    if created and instance.visitor.email_address and not instance.email_sent:
        try:
            send_subsequent_visit_email(instance.visitor, instance)
            logger.info(f"Return visit email sent to visitor: {instance.visitor.full_name}")
        except Exception as e:
            logger.error(f"Failed to send return visit email to {instance.visitor.full_name}: {str(e)}")
