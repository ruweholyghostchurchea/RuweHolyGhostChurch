from django.db.models.signals import post_save
from django.dispatch import receiver
from members.models import Member
from .utils import send_welcome_email
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Member)
def send_welcome_email_on_registration(sender, instance, created, **kwargs):
    """
    Automatically send welcome email when a new member is registered
    """
    if created and instance.email_address:
        try:
            logger.info(f"Sending welcome email to new member: {instance.full_name} ({instance.email_address})")
            send_welcome_email(instance)
        except Exception as e:
            logger.error(f"Failed to send welcome email to {instance.full_name}: {str(e)}")
