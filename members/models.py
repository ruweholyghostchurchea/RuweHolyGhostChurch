
from django.db import models
from church_structure.models import Diocese, Pastorate, Church

class Member(models.Model):
    USER_GROUP_CHOICES = [
        ('Youth', 'Youth'),
        ('Adult', 'Adult'),
        ('Elder', 'Elder'),
        ('Clergy', 'Clergy'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    user_group = models.CharField(max_length=20, choices=USER_GROUP_CHOICES)
    date_of_birth = models.DateField()
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
