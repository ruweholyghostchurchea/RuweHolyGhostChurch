from django.db import models
from django.contrib.auth.models import User
from members.models import Member
import json


class EmailTemplate(models.Model):
    """Pre-defined email templates for common communications"""
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Email'),
        ('announcement', 'General Announcement'),
        ('event', 'Event Notification'),
        ('newsletter', 'Newsletter'),
        ('reminder', 'Reminder'),
        ('custom', 'Custom Template'),
    ]
    
    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES, default='custom')
    subject = models.CharField(max_length=300)
    html_content = models.TextField(help_text="HTML email content with placeholders")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    class Meta:
        ordering = ['-created_at']


class EmailCampaign(models.Model):
    """Email campaigns to send bulk emails to members"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    RECIPIENT_TYPE_CHOICES = [
        ('all', 'All Members'),
        ('youth', 'Youth Only'),
        ('adult', 'Adults Only'),
        ('elder', 'Elders Only'),
        ('clergy', 'Clergy Only'),
        ('staff', 'Staff Only'),
        ('ordained', 'Ordained Members Only'),
        ('diocese', 'Specific Diocese'),
        ('pastorate', 'Specific Pastorate'),
        ('church', 'Specific Church'),
        ('custom', 'Custom Filter'),
        ('custom_emails', 'Custom Email Addresses'),
    ]
    
    name = models.CharField(max_length=200, help_text="Campaign name for internal reference")
    subject = models.CharField(max_length=300)
    html_content = models.TextField(help_text="HTML email content")
    recipient_type = models.CharField(max_length=50, choices=RECIPIENT_TYPE_CHOICES, default='all')
    recipient_filter = models.JSONField(default=dict, blank=True, help_text="Additional filters for recipients")
    custom_emails = models.JSONField(default=list, blank=True, help_text="Custom email addresses for sending")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    class Meta:
        ordering = ['-created_at']


class EmailCampaignAttachment(models.Model):
    """Attachments for email campaigns"""
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='email_attachments/%Y/%m/', help_text="Document or photo attachment")
    filename = models.CharField(max_length=255, help_text="Original filename")
    file_size = models.IntegerField(help_text="File size in bytes")
    content_type = models.CharField(max_length=100, help_text="MIME content type")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.filename} ({self.campaign.name})"
    
    class Meta:
        ordering = ['created_at']


class EmailLog(models.Model):
    """Log of individual emails sent"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]
    
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name='email_logs', null=True, blank=True)
    recipient = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=200)
    
    subject = models.CharField(max_length=300)
    html_content = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Tracking
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.recipient_email} - {self.subject} ({self.get_status_display()})"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient_email']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
