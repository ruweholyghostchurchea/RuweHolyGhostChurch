"""
Utility functions for the Attendance app.
Includes absence tracking, email notifications, and statistics.
"""

from django.template.loader import render_to_string
from django.utils import timezone
from email_system.utils import send_html_email
from .models import AbsenceStreak, AttendanceRecord
import logging

logger = logging.getLogger(__name__)


def check_and_update_absence_streak(member, church, session, status):
    """
    Check and update absence streak for a member.
    Send email if 3 consecutive absences reached.
    
    Args:
        member: Member instance
        church: Church instance
        session: AttendanceSession instance
        status: Attendance status ('present', 'apology', 'absent')
        
    Returns:
        Boolean indicating if email was sent
    """
    # Get or create absence streak record
    streak, created = AbsenceStreak.objects.get_or_create(
        member=member,
        church=church
    )
    
    # Update streak based on status
    if status == 'present' or status == 'apology':
        # Reset streak if present or apology
        streak.reset_streak()
        return False
    
    elif status == 'absent':
        # Increment streak
        should_send_email = streak.increment_streak(session.session_date)
        
        # Send email if 3 consecutive absences
        if should_send_email:
            email_sent = send_absence_notification_email(member, streak)
            if email_sent:
                streak.email_sent_for_3_absences = True
                streak.email_sent_date = timezone.now().date()
                streak.save()
                return True
    
    return False


def send_absence_notification_email(member, streak):
    """
    Send email notification to member after 3 consecutive absences.
    
    Args:
        member: Member instance
        streak: AbsenceStreak instance
        
    Returns:
        EmailLog instance or None
    """
    if not member.email_address:
        logger.warning(f"Cannot send absence email to {member.full_name}: No email address")
        return None
    
    # Prepare email content
    context = {
        'member': member,
        'streak': streak,
        'church_name': streak.church.name if streak.church else 'Ruwe Holy Ghost Church EA',
    }
    
    # Create HTML content
    html_content = f"""
    <h2>We've Missed You at {context['church_name']}</h2>
    <p>Dear {member.full_name},</p>
    
    <p>We've noticed that you haven't been able to join us for our recent Sabbath services, 
    and we wanted to reach out to let you know that you've been missed.</p>
    
    <p><strong>Our records show you've been absent for {streak.current_streak} consecutive services.</strong></p>
    
    <p>We understand that life can get busy, and circumstances sometimes prevent us from 
    attending church. We want you to know that we're thinking of you and praying for you.</p>
    
    <h3>How Can We Help?</h3>
    <p>If there's anything we can do to support you, or if you're facing challenges that 
    we can pray about, please don't hesitate to reach out to us. We're here for you.</p>
    
    <p>We'd love to see you back with us soon! Our Sabbath services are held every Saturday 
    at 6:00 AM, 9:00 AM, 12:00 PM, and 3:00 PM.</p>
    
    <p>You are an important part of our church family, and your presence is valued.</p>
    
    <p>With love and prayers,<br>
    <strong>{context['church_name']}</strong></p>
    """
    
    subject = f"We've Missed You - {context['church_name']}"
    
    return send_html_email(
        subject=subject,
        html_content=html_content,
        recipient_email=member.email_address,
        recipient_name=member.full_name,
        context=context
    )


def calculate_attendance_statistics(level='church', church=None, pastorate=None, diocese=None, start_date=None, end_date=None):
    """
    Calculate attendance statistics for a given hierarchy level and date range.
    
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
    from .models import AttendanceSession, AttendanceRecord, AbsenceStreak
    from members.models import Member
    from django.db.models import Q, Count, Avg
    
    # Build query for sessions based on level
    session_query = Q()
    
    if level == 'church' and church:
        session_query = Q(church=church)
    elif level == 'pastorate' and pastorate:
        session_query = Q(pastorate=pastorate)
    elif level == 'diocese' and diocese:
        session_query = Q(diocese=diocese)
    elif level == 'dean':
        session_query = Q(is_dean_session=True)
    
    # Add date filter
    if start_date:
        session_query &= Q(session_date__gte=start_date)
    if end_date:
        session_query &= Q(session_date__lte=end_date)
    
    # Get sessions
    sessions = AttendanceSession.objects.filter(session_query)
    
    # Get attendance records for these sessions
    records = AttendanceRecord.objects.filter(session__in=sessions)
    
    # Get absence streaks
    streak_query = Q()
    if church:
        streak_query = Q(church=church)
    absence_streaks = AbsenceStreak.objects.filter(streak_query, current_streak__gte=3)
    
    # Calculate statistics
    stats = {
        'total_sessions': sessions.count(),
        'total_attendance_records': records.count(),
        'total_present': records.filter(status='present').count(),
        'total_apology': records.filter(status='apology').count(),
        'total_absent': records.filter(status='absent').count(),
        'average_attendance_rate': 0.0,
        'active_members': records.filter(status='present').values('member').distinct().count(),
        'inactive_members': absence_streaks.count(),
    }
    
    # Calculate average attendance rate
    if stats['total_attendance_records'] > 0:
        stats['average_attendance_rate'] = round(
            (stats['total_present'] / stats['total_attendance_records']) * 100, 2
        )
    
    return stats


def bulk_mark_attendance(session, member_ids, status, marked_by=None):
    """
    Bulk mark attendance for multiple members in a session.
    
    Args:
        session: AttendanceSession instance
        member_ids: List of member IDs
        status: Attendance status ('present', 'apology', 'absent')
        marked_by: User who is marking (optional)
        
    Returns:
        Number of records created/updated
    """
    from members.models import Member
    
    count = 0
    for member_id in member_ids:
        try:
            member = Member.objects.get(id=member_id)
            
            # Create or update attendance record
            record, created = AttendanceRecord.objects.update_or_create(
                session=session,
                member=member,
                defaults={
                    'status': status,
                    'marked_by': marked_by
                }
            )
            
            # Check and update absence streak if church level
            if session.church:
                check_and_update_absence_streak(
                    member=member,
                    church=session.church,
                    session=session,
                    status=status
                )
            
            count += 1
        except Member.DoesNotExist:
            logger.warning(f"Member with ID {member_id} not found")
            continue
    
    # Update session statistics
    session.update_statistics()
    
    return count
