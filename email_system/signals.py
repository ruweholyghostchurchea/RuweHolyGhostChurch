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
            from django.forms.models import model_to_dict
            old_instance = Member.objects.get(pk=instance.pk)
            
            old_data = model_to_dict(old_instance, exclude=['created_at', 'updated_at', 'profile_photo'])
            new_data = model_to_dict(instance, exclude=['created_at', 'updated_at', 'profile_photo'])
            
            instance._data_changed = old_data != new_data
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
