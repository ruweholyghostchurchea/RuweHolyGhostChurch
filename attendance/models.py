
from django.db import models
from members.models import Member

class Service(models.Model):
    SERVICE_TYPES = [
        ('saturday_morning', 'Saturday Morning Sabbath'),
        ('saturday_evening', 'Saturday Evening Service'),
        ('wednesday', 'Wednesday Service'),
        ('prayer_meeting', 'Prayer Meeting'),
        ('bible_study', 'Bible Study'),
        ('youth_service', 'Youth Service'),
        ('special_event', 'Special Event'),
    ]
    
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, default='Main Church, Ruwe, Siaya County')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
        
    def __str__(self):
        return f"{self.name} - {self.date}"

class Attendance(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='attendances')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    present = models.BooleanField(default=True)
    check_in_time = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['service', 'member']
        ordering = ['service', 'member__last_name']
        
    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.member.full_name} - {self.service.name} ({status})"
