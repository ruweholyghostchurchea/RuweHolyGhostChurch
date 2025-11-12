from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from members.models import Member
from .utils import send_welcome_email, send_member_update_email
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Member)
def track_member_changes(sender, instance, **kwargs):
    """
    Track if member data has changed before saving
    """
    if instance.pk:
        try:
            old_instance = Member.objects.get(pk=instance.pk)
            instance._data_changed = (
                old_instance.first_name != instance.first_name or
                old_instance.last_name != instance.last_name or
                old_instance.email_address != instance.email_address or
                old_instance.phone_number != instance.phone_number or
                old_instance.user_home_church_id != instance.user_home_church_id or
                old_instance.member_roles != instance.member_roles
            )
        except Member.DoesNotExist:
            instance._data_changed = False
    else:
        instance._data_changed = False


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


@receiver(post_save, sender=Member)
def send_update_email_on_member_change(sender, instance, created, **kwargs):
    """
    Send email notification when member details are updated
    """
    if not created and hasattr(instance, '_data_changed') and instance._data_changed and instance.email_address:
        try:
            logger.info(f"Sending update email to member: {instance.full_name} ({instance.email_address})")
            send_member_update_email(instance)
        except Exception as e:
            logger.error(f"Failed to send update email to {instance.full_name}: {str(e)}")
