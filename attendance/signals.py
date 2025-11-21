"""
Signals for the Attendance app.
Handles automatic absence streak tracking and email notifications.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AttendanceRecord, AttendanceSession
from .utils import check_and_update_absence_streak
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AttendanceRecord)
def update_absence_streak(sender, instance, created, **kwargs):
    """
    Update absence streak when attendance record is created or updated.
    Sends email notification if member has 3 consecutive absences.
    Tracks absences across all hierarchy levels.
    """
    # Determine which church to track for (from session hierarchy)
    tracking_church = None
    
    if instance.session.church:
        # Direct church-level session
        tracking_church = instance.session.church
    elif instance.session.pastorate and hasattr(instance.member, 'user_home_church'):
        # Pastorate-level session - use member's home church
        tracking_church = instance.member.user_home_church
    elif instance.session.diocese and hasattr(instance.member, 'user_home_church'):
        # Diocese-level session - use member's home church
        tracking_church = instance.member.user_home_church
    elif instance.session.is_dean_session and hasattr(instance.member, 'user_home_church'):
        # Dean-level session - use member's home church
        tracking_church = instance.member.user_home_church
    
    # Track absence streak if we have a church
    if tracking_church:
        try:
            # Check and update absence streak
            email_sent = check_and_update_absence_streak(
                member=instance.member,
                church=tracking_church,
                session=instance.session,
                status=instance.status
            )
            
            if email_sent:
                logger.info(f"Absence notification email sent to: {instance.member.full_name}")
        except Exception as e:
            logger.error(f"Failed to update absence streak for {instance.member.full_name}: {str(e)}")


@receiver(post_save, sender=AttendanceRecord)
def update_session_statistics(sender, instance, **kwargs):
    """
    Update session statistics whenever an attendance record is saved.
    """
    try:
        instance.session.update_statistics()
        logger.info(f"Updated statistics for session: {instance.session.session_name}")
    except Exception as e:
        logger.error(f"Failed to update session statistics: {str(e)}")
