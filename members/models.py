
from django.db import models
from church_structure.models import Diocese, Pastorate, Church
import json

class Member(models.Model):
    USER_GROUP_CHOICES = [
        ('Youth', 'Youth'),
        ('Adult', 'Adult'),
        ('Elder', 'Elder'),
        ('Clergy', 'Clergy'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    ]
    
    LOCATION_CHOICES = [
        ('siaya', 'Siaya'),
        ('nairobi', 'Nairobi'),
        ('kisumu', 'Kisumu'),
        ('mombasa', 'Mombasa'),
        ('nakuru', 'Nakuru'),
        ('eldoret', 'Eldoret'),
        ('other', 'Other'),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('primary', 'Primary Education'),
        ('secondary', 'Secondary Education'),
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    user_group = models.CharField(max_length=20, choices=USER_GROUP_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='single')
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='other')
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, default='other')
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField(blank=True)
    
    # Job/Occupation Information
    job_occupation_income = models.TextField(help_text="Job title, occupation details, and income information")
    
    # Baptismal Information
    baptismal_first_name = models.CharField(max_length=100)
    baptismal_last_name = models.CharField(max_length=100)
    date_baptized = models.DateField()
    date_joined_religion = models.DateField()
    date_joined_app = models.DateField(auto_now_add=True)
    
    # Home Church Structure (Required)
    user_home_diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, related_name='home_members')
    user_home_pastorate = models.ForeignKey(Pastorate, on_delete=models.CASCADE, related_name='home_members')
    user_home_church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='home_members')
    
    # Town Church Structure (Optional - for work/education/treatment)
    user_town_diocese = models.ForeignKey(Diocese, on_delete=models.SET_NULL, null=True, blank=True, related_name='town_members')
    user_town_pastorate = models.ForeignKey(Pastorate, on_delete=models.SET_NULL, null=True, blank=True, related_name='town_members')
    user_town_church = models.ForeignKey(Church, on_delete=models.SET_NULL, null=True, blank=True, related_name='town_members')
    
    # Emergency Contacts
    emergency_contact_1_name = models.CharField(max_length=100, blank=True)
    emergency_contact_1_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_1_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_1_email = models.EmailField(blank=True)
    
    emergency_contact_2_name = models.CharField(max_length=100, blank=True)
    emergency_contact_2_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_2_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_2_email = models.EmailField(blank=True)
    
    # Profile Photo
    profile_photo = models.ImageField(upload_to='member_photos/', blank=True, null=True)
    profile_photo_url = models.URLField(blank=True, help_text="Alternative to uploading a photo")
    
    # Custom Fields (JSON field for flexible custom data)
    custom_fields = models.JSONField(default=dict, blank=True, help_text="Store custom member data as key-value pairs")
    
    # System fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def baptismal_full_name(self):
        return f"{self.baptismal_first_name} {self.baptismal_last_name}"
    
    @property
    def home_church_hierarchy(self):
        return f"{self.user_home_diocese.name} > {self.user_home_pastorate.name} > {self.user_home_church.name}"
    
    @property
    def town_church_hierarchy(self):
        if self.user_town_church:
            return f"{self.user_town_diocese.name} > {self.user_town_pastorate.name} > {self.user_town_church.name}"
        return "Not assigned"
    
    @property
    def display_photo(self):
        """Return the profile photo URL or uploaded photo URL"""
        if self.profile_photo:
            return self.profile_photo.url
        elif self.profile_photo_url:
            return self.profile_photo_url
        return None
    
    def get_custom_field(self, key, default=None):
        """Get a custom field value by key"""
        return self.custom_fields.get(key, default)
    
    def set_custom_field(self, key, value):
        """Set a custom field value"""
        self.custom_fields[key] = value


class MemberDocument(models.Model):
    DOCUMENT_TYPES = [
        ('baptism_certificate', 'Baptism Certificate'),
        ('annual_tithe_card', 'Annual Tithe Card'),
        ('id_document', 'ID Document'),
        ('medical_record', 'Medical Record'),
        ('membership_certificate', 'Membership Certificate'),
        ('other', 'Other'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_file = models.FileField(upload_to='member_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=100, blank=True)  # Could be linked to User model later
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Member Document'
        verbose_name_plural = 'Member Documents'
    
    def __str__(self):
        return f"{self.member.full_name} - {self.title}"
