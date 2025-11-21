from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese
import random
import string


class AttendanceSession(models.Model):
    """
    Represents a church service/gathering session for attendance tracking.
    Can be at Church, Pastorate, Diocese, or Dean/Headquarters level.
    """
    
    # Session type choices
    SESSION_TYPE_CHOICES = [
        ('sabbath', 'Saturday Sabbath Service'),
        ('weekday', 'Weekday Service'),
        ('prayer_meeting', 'Prayer Meeting'),
        ('bible_study', 'Bible Study'),
        ('youth_service', 'Youth Service'),
        ('special_event', 'Special Event'),
        ('pastorate_gathering', 'Pastorate Gathering'),
        ('diocese_gathering', 'Diocese Gathering'),
        ('dean_gathering', 'Dean/Headquarters Gathering'),
    ]
    
    # Hierarchy level choices
    LEVEL_CHOICES = [
        ('church', 'Church Level'),
        ('pastorate', 'Pastorate Level'),
        ('diocese', 'Diocese Level'),
        ('dean', 'Dean/Headquarters Level'),
    ]
    
    # Service time choices (primarily for Saturday Sabbath)
    SERVICE_TIME_CHOICES = [
        ('6:00 AM', '6:00 AM Saturday'),
        ('9:00 AM', '9:00 AM Saturday'),
        ('12:00 PM', '12:00 PM Saturday'),
        ('3:00 PM', '3:00 PM Saturday'),
        ('Other', 'Other Time'),
    ]
    
    # Basic Information
    session_code = models.CharField(max_length=20, unique=True, blank=True, 
                                   help_text="Auto-generated session code (e.g., RUWE-SESS-XXXX-XXXX)")
    session_name = models.CharField(max_length=200, help_text="Session name (e.g., Sabbath Service - Jan 15, 2025)")
    session_type = models.CharField(max_length=30, choices=SESSION_TYPE_CHOICES, default='sabbath')
    session_date = models.DateField(default=timezone.now)
    service_time = models.CharField(max_length=20, choices=SERVICE_TIME_CHOICES, default='9:00 AM')
    
    # Hierarchy - where this session is held
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='church')
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='attendance_sessions',
                              help_text="Church (for church-level sessions)")
    pastorate = models.ForeignKey(Pastorate, on_delete=models.CASCADE, null=True, blank=True, 
                                 related_name='attendance_sessions',
                                 help_text="Pastorate (for pastorate-level sessions)")
    diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='attendance_sessions',
                               help_text="Diocese (for diocese-level sessions)")
    is_dean_session = models.BooleanField(default=False, 
                                         verbose_name="Dean/Headquarters Session",
                                         help_text="Session at Dean/Headquarters level")
    
    # Session details
    location = models.CharField(max_length=300, blank=True, 
                               help_text="Specific location/venue")
    preacher = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='preached_sessions',
                                help_text="Who preached/led this session")
    topic = models.CharField(max_length=300, blank=True, help_text="Sermon/teaching topic")
    notes = models.TextField(blank=True, help_text="Session notes")
    
    # Statistics (auto-calculated)
    total_expected = models.IntegerField(default=0, help_text="Expected attendance count")
    total_present = models.IntegerField(default=0, help_text="Present count")
    total_apology = models.IntegerField(default=0, help_text="Apology count")
    total_absent = models.IntegerField(default=0, help_text="Absent count")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False, 
                                   help_text="Lock session to prevent further changes")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-session_date', '-service_time']
        verbose_name = 'Attendance Session'
        verbose_name_plural = 'Attendance Sessions'
        indexes = [
            models.Index(fields=['session_code']),
            models.Index(fields=['-session_date']),
            models.Index(fields=['level']),
        ]
    
    def __str__(self):
        return f"{self.session_name} - {self.session_date}"
    
    @property
    def attendance_percentage(self):
        """Calculate attendance percentage"""
        if self.total_expected > 0:
            return round((self.total_present / self.total_expected) * 100, 1)
        return 0
    
    @property
    def hierarchy_display(self):
        """Display which hierarchy level this session belongs to"""
        if self.is_dean_session:
            return "Dean/Headquarters"
        elif self.diocese and not self.pastorate and not self.church:
            return f"Diocese: {self.diocese.name}"
        elif self.pastorate and not self.church:
            return f"Pastorate: {self.pastorate.name}"
        elif self.church:
            return f"Church: {self.church.name}"
        return "Unknown"
    
    def generate_session_code(self):
        """Generate a unique session code (e.g., RUWE-SESS-XXXX-XXXX)"""
        while True:
            # Generate random 4-character segments
            segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            session_code = f"RUWE-SESS-{segment1}-{segment2}"
            
            # Check if this session code already exists
            if not AttendanceSession.objects.filter(session_code=session_code).exists():
                return session_code
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate session code"""
        # Generate session code if not exists
        if not self.session_code:
            self.session_code = self.generate_session_code()
        
        super().save(*args, **kwargs)
    
    def update_statistics(self):
        """Update attendance statistics for this session"""
        records = self.attendance_records.all()
        self.total_expected = records.count()
        self.total_present = records.filter(status='present').count()
        self.total_apology = records.filter(status='apology').count()
        self.total_absent = records.filter(status='absent').count()
        self.save()


class AttendanceRecord(models.Model):
    """
    Individual attendance record for a member in a specific session.
    """
    
    # Attendance status choices
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('apology', 'Apology'),
        ('absent', 'Absent'),
    ]
    
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, 
                               related_name='attendance_records')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, 
                              related_name='attendance_records')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    
    # Details
    check_in_time = models.TimeField(null=True, blank=True, 
                                     help_text="Time member checked in (if present)")
    apology_reason = models.TextField(blank=True, 
                                     help_text="Reason for apology (if applicable)")
    notes = models.TextField(blank=True, help_text="Additional notes")
    
    # System fields
    marked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 help_text="Who marked this attendance")
    
    class Meta:
        ordering = ['member__last_name', 'member__first_name']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['session', 'member']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-marked_at']),
        ]
    
    def __str__(self):
        return f"{self.member.full_name} - {self.session.session_name} ({self.get_status_display()})"


class AbsenceStreak(models.Model):
    """
    Track consecutive absence streaks for members.
    Used to trigger email notifications after 3 consecutive absences.
    """
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, 
                              related_name='absence_streaks')
    church = models.ForeignKey(Church, on_delete=models.CASCADE, 
                              related_name='absence_streaks',
                              help_text="Church where absences are tracked")
    
    # Streak tracking
    current_streak = models.IntegerField(default=0, 
                                        help_text="Current consecutive absence count")
    last_absence_date = models.DateField(null=True, blank=True)
    last_present_date = models.DateField(null=True, blank=True)
    
    # Email notification tracking
    email_sent_for_3_absences = models.BooleanField(default=False)
    email_sent_date = models.DateField(null=True, blank=True)
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Absence Streak'
        verbose_name_plural = 'Absence Streaks'
        unique_together = ['member', 'church']
    
    def __str__(self):
        return f"{self.member.full_name} - {self.current_streak} consecutive absences"
    
    def reset_streak(self):
        """Reset the absence streak when member attends"""
        self.current_streak = 0
        self.email_sent_for_3_absences = False
        self.last_present_date = timezone.now().date()
        self.save()
    
    def increment_streak(self, absence_date):
        """Increment absence streak"""
        self.current_streak += 1
        self.last_absence_date = absence_date
        self.save()
        
        # Check if we need to send notification email
        if self.current_streak >= 3 and not self.email_sent_for_3_absences:
            return True  # Signal that email should be sent
        return False


class AttendanceStatistics(models.Model):
    """
    Aggregated attendance statistics for reporting across the church hierarchy.
    """
    
    # Hierarchy level
    LEVEL_CHOICES = [
        ('church', 'Church Level'),
        ('pastorate', 'Pastorate Level'),
        ('diocese', 'Diocese Level'),
        ('dean', 'Dean/Headquarters Level'),
    ]
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True, blank=True)
    pastorate = models.ForeignKey(Pastorate, on_delete=models.CASCADE, null=True, blank=True)
    diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, null=True, blank=True)
    
    # Statistics period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Attendance metrics
    total_sessions = models.IntegerField(default=0)
    total_attendance_records = models.IntegerField(default=0)
    total_present = models.IntegerField(default=0)
    total_apology = models.IntegerField(default=0)
    total_absent = models.IntegerField(default=0)
    average_attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,
                                                  help_text="Average attendance percentage")
    
    # Member engagement
    active_members = models.IntegerField(default=0, 
                                        help_text="Members who attended at least once")
    inactive_members = models.IntegerField(default=0, 
                                          help_text="Members with 3+ consecutive absences")
    
    # Generated date
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-period_end']
        verbose_name = 'Attendance Statistics'
        verbose_name_plural = 'Attendance Statistics'
    
    def __str__(self):
        level_name = self.church or self.pastorate or self.diocese or "Dean"
        return f"{level_name} - {self.period_start} to {self.period_end}"
