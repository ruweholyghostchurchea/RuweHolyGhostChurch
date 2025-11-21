from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese
import random
import string


class Visitor(models.Model):
    """
    Complete visitor profile for church visitors.
    Tracks visitor information across the church hierarchy.
    """
    
    # Gender choices
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    # Marital status choices
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    ]
    
    # Age group choices
    AGE_GROUP_CHOICES = [
        ('child', 'Child (0-12)'),
        ('youth', 'Youth (13-25)'),
        ('adult', 'Adult (26-59)'),
        ('elder', 'Elder (60+)'),
    ]
    
    # How they heard about us choices
    REFERRAL_SOURCE_CHOICES = [
        ('member', 'Church Member'),
        ('friend', 'Friend/Family'),
        ('social_media', 'Social Media'),
        ('website', 'Website'),
        ('passing_by', 'Passing By'),
        ('event', 'Event/Crusade'),
        ('other', 'Other'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=20, unique=True, blank=True, 
                                  help_text="Auto-generated unique identifier (e.g., RUWE-VSTR-XXXX-XXXX)")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES, default='adult')
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='single')
    
    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)
    physical_address = models.TextField(blank=True, help_text="Physical address/location")
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Kenya')
    
    # Church Hierarchy - where they visited
    church = models.ForeignKey(Church, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='visitors', help_text="Church where visitor came")
    pastorate = models.ForeignKey(Pastorate, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='visitors', help_text="Pastorate (auto-filled from church)")
    diocese = models.ForeignKey(Diocese, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='visitors', help_text="Diocese (auto-filled from church)")
    is_dean_visitor = models.BooleanField(default=False, 
                                         verbose_name="Dean/Headquarters Visitor",
                                         help_text="Visitor came during Dean/Headquarters gathering")
    
    # First Visit Information
    first_visit_date = models.DateField(default=timezone.now)
    referral_source = models.CharField(max_length=50, choices=REFERRAL_SOURCE_CHOICES, default='other')
    invited_by_member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, 
                                         related_name='invited_visitors',
                                         help_text="Member who invited this visitor")
    invited_by_name = models.CharField(max_length=200, blank=True, 
                                      help_text="Name of person who invited (if not a member)")
    
    # Interest & Engagement
    interested_in_membership = models.BooleanField(default=False)
    prayer_request = models.TextField(blank=True)
    interests = models.TextField(blank=True, help_text="Ministry interests (Youth, Choir, etc.)")
    
    # Conversion tracking
    converted_to_member = models.BooleanField(default=False)
    converted_date = models.DateField(null=True, blank=True)
    member_profile = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='converted_from_visitor',
                                      help_text="Link to member profile if converted")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Active visitor (not converted yet)")
    
    # Notes
    notes = models.TextField(blank=True, help_text="Additional notes about this visitor")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='created_visitors')
    
    class Meta:
        ordering = ['-first_visit_date', '-created_at']
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'
        indexes = [
            models.Index(fields=['identifier']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['email_address']),
            models.Index(fields=['-first_visit_date']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.identifier}"
    
    @property
    def full_name(self):
        """Return visitor's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def visit_count(self):
        """Return total number of visits"""
        return self.visits.count()
    
    @property
    def last_visit_date(self):
        """Return date of most recent visit"""
        latest_visit = self.visits.order_by('-visit_date').first()
        if latest_visit:
            return latest_visit.visit_date
        return self.first_visit_date
    
    @property
    def follow_up_count(self):
        """Return number of follow-up attempts"""
        return self.follow_ups.count()
    
    @property
    def last_follow_up(self):
        """Return most recent follow-up"""
        return self.follow_ups.order_by('-follow_up_date').first()
    
    def generate_identifier(self):
        """Generate a unique identifier for the visitor (e.g., RUWE-VSTR-XXXX-XXXX)"""
        while True:
            # Generate random 4-character segments
            segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            identifier = f"RUWE-VSTR-{segment1}-{segment2}"
            
            # Check if this identifier already exists
            if not Visitor.objects.filter(identifier=identifier).exists():
                return identifier
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate identifier and populate hierarchy"""
        # Generate identifier if not exists
        if not self.identifier:
            self.identifier = self.generate_identifier()
        
        # Auto-populate pastorate and diocese from church
        if self.church:
            self.pastorate = self.church.pastorate
            self.diocese = self.church.pastorate.diocese
        
        super().save(*args, **kwargs)


class VisitorVisit(models.Model):
    """
    Record of each visit by a visitor (2nd, 3rd, subsequent visits).
    First visit is tracked in the Visitor model itself.
    """
    
    # Visit type choices
    VISIT_TYPE_CHOICES = [
        ('sabbath', 'Saturday Sabbath Service'),
        ('weekday', 'Weekday Service'),
        ('event', 'Special Event/Crusade'),
        ('meeting', 'Meeting'),
        ('counseling', 'Counseling Session'),
        ('other', 'Other'),
    ]
    
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='visits')
    visit_number = models.PositiveIntegerField(help_text="Visit number (2, 3, 4, etc.)")
    visit_date = models.DateField(default=timezone.now)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES, default='sabbath')
    
    # Attendance details
    service_attended = models.CharField(max_length=200, blank=True, 
                                       help_text="Service/event attended (e.g., 9:00 AM Sabbath)")
    came_with = models.CharField(max_length=200, blank=True, 
                                help_text="Who they came with")
    
    # Follow-up
    notes = models.TextField(blank=True, help_text="Notes about this visit")
    email_sent = models.BooleanField(default=False, help_text="Follow-up email sent for this visit")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-visit_date']
        verbose_name = 'Visitor Visit'
        verbose_name_plural = 'Visitor Visits'
        unique_together = ['visitor', 'visit_number']
    
    def __str__(self):
        return f"{self.visitor.full_name} - Visit #{self.visit_number} ({self.visit_date})"


class VisitorFollowUp(models.Model):
    """
    Track follow-up attempts and communications with visitors.
    """
    
    # Follow-up method choices
    FOLLOW_UP_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('sms', 'SMS/Text Message'),
        ('home_visit', 'Home Visit'),
        ('church_visit', 'Church Visit'),
        ('whatsapp', 'WhatsApp'),
        ('other', 'Other'),
    ]
    
    # Follow-up status choices
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('unsuccessful', 'Unsuccessful'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='follow_ups')
    follow_up_method = models.CharField(max_length=20, choices=FOLLOW_UP_METHOD_CHOICES)
    follow_up_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Details
    purpose = models.CharField(max_length=200, blank=True, 
                              help_text="Purpose of follow-up (e.g., Thank you for visiting)")
    notes = models.TextField(blank=True, help_text="Follow-up notes and outcome")
    next_follow_up_date = models.DateField(null=True, blank=True, 
                                          help_text="Schedule next follow-up")
    
    # If email follow-up, link to email log
    email_campaign = models.ForeignKey('email_system.EmailCampaign', on_delete=models.SET_NULL, 
                                      null=True, blank=True, related_name='visitor_follow_ups')
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-follow_up_date']
        verbose_name = 'Visitor Follow-Up'
        verbose_name_plural = 'Visitor Follow-Ups'
    
    def __str__(self):
        return f"{self.visitor.full_name} - {self.get_follow_up_method_display()} ({self.follow_up_date})"


class VisitorStatistics(models.Model):
    """
    Aggregated visitor statistics for reporting.
    Can be calculated on-demand or cached periodically.
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
    
    # Statistics
    period_start = models.DateField()
    period_end = models.DateField()
    total_visitors = models.IntegerField(default=0)
    first_time_visitors = models.IntegerField(default=0)
    return_visitors = models.IntegerField(default=0)
    converted_to_members = models.IntegerField(default=0)
    
    # Demographics
    male_count = models.IntegerField(default=0)
    female_count = models.IntegerField(default=0)
    youth_count = models.IntegerField(default=0)
    adult_count = models.IntegerField(default=0)
    elder_count = models.IntegerField(default=0)
    
    # Generated date
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-period_end']
        verbose_name = 'Visitor Statistics'
        verbose_name_plural = 'Visitor Statistics'
    
    def __str__(self):
        level_name = self.church or self.pastorate or self.diocese or "Dean"
        return f"{level_name} - {self.period_start} to {self.period_end}"
