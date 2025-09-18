
from django.db import models

class ChurchInfo(models.Model):
    name = models.CharField(max_length=200, default='RuweHolyGhostChurch')
    tagline = models.CharField(max_length=300, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Pastor Information
    pastor_name = models.CharField(max_length=200)
    pastor_phone = models.CharField(max_length=20, blank=True)
    pastor_email = models.EmailField(blank=True)
    
    # Service Times
    sunday_morning_service = models.TimeField(default='09:00')
    sunday_evening_service = models.TimeField(default='18:00')
    wednesday_service = models.TimeField(default='19:00')
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # System Settings
    enable_sms = models.BooleanField(default=True)
    sms_sender_name = models.CharField(max_length=11, blank=True)
    auto_backup = models.BooleanField(default=True)
    
    # Logo and Images
    logo = models.URLField(blank=True, null=True, help_text='Church logo URL')
    banner_image = models.URLField(blank=True, null=True, help_text='Church banner image URL')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Church Information'
        verbose_name_plural = 'Church Information'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and ChurchInfo.objects.exists():
            raise ValueError('Only one ChurchInfo instance is allowed')
        super().save(*args, **kwargs)

class SystemSettings(models.Model):
    # Notification Settings
    birthday_notifications = models.BooleanField(default=True)
    anniversary_notifications = models.BooleanField(default=True)
    attendance_reminders = models.BooleanField(default=True)
    follow_up_reminders = models.BooleanField(default=True)
    
    # Email Settings
    smtp_server = models.CharField(max_length=200, blank=True)
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_username = models.CharField(max_length=200, blank=True)
    smtp_password = models.CharField(max_length=200, blank=True)
    smtp_use_tls = models.BooleanField(default=True)
    
    # SMS Settings
    sms_api_key = models.CharField(max_length=200, blank=True)
    sms_api_secret = models.CharField(max_length=200, blank=True)
    sms_provider = models.CharField(max_length=50, default='twilio')
    
    # Backup Settings
    backup_frequency = models.CharField(max_length=20, default='weekly')
    backup_location = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Settings'
        verbose_name_plural = 'System Settings'
        
    def __str__(self):
        return 'System Settings'
