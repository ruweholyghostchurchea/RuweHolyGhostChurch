
from django.db import models

class Visitor(models.Model):
    VISIT_PURPOSE = [
        ('service', 'Church Service'),
        ('event', 'Special Event'),
        ('meeting', 'Meeting'),
        ('counseling', 'Counseling'),
        ('other', 'Other'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    
    # Visit Information
    visit_date = models.DateField(auto_now_add=True)
    visit_purpose = models.CharField(max_length=20, choices=VISIT_PURPOSE, default='service')
    invited_by = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=True)
    follow_up_completed = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_date']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.visit_date}"
