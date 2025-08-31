
from django.db import models
from church_structure.models import Diocese, Pastorate, Church
import json
import random
import string

class Member(models.Model):
    USER_GROUP_CHOICES = [
        ('Youth', 'Youth'),
        ('Adult', 'Adult'),
        ('Elder', 'Elder'),
    ]
    
    MEMBER_ROLES = [
        ('regular_member', 'Regular Member'),
        ('singer', 'Singer'),
        ('drum_percussionist', 'Drum Percussionist'),
        ('shaker_percussionist', 'Shaker Percussionist'),
        ('synod_representative', 'Synod Representative'),
        ('clergy', 'Clergy'),
    ]
    
    CHURCH_CLERGY_ROLES = [
        ('church_teacher_wife', "Teacher's Wife"),
        ('church_teacher_husband', "Teacher's Husband"),
        ('church_teacher', 'Teacher'),
        ('pastorate_woman_leader', 'Woman Leader'),
        ('pastorate_woman_leader_husband', "Woman Leader's Husband"),
        ('pastorate_division_wife', "Division's Wife"),
        ('pastorate_division_husband', "Division's Husband"),
        ('pastorate_division', 'Division'),
        ('pastorate_lay_reader_wife', "Lay Reader's Wife"),
        ('pastorate_lay_reader', 'Lay Reader'),
        ('pastorate_pastor_wife', "Pastor's Wife"),
        ('pastorate_pastor', 'Pastor'),
        ('diocese_bishop_wife', "Bishop's Wife"),
        ('diocese_bishop', 'Bishop'),
        ('dean_archbishop_wife', "Archbishop's Wife"),
        ('dean_archbishop', 'Archbishop'),
    ]
    
    SPECIAL_CLERGY_ROLES = [
        ('dean_king', 'King'),
        ('dean_king_wife', "King's Wife"),
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
    
    MEMBERSHIP_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Transferred', 'Transferred'),
        ('Left/Quit', 'Left/Quit'),
        ('Dead', 'Dead'),
    ]
    
    PWD_TYPE_CHOICES = [
        ('prefer_not_to_say', 'Prefer not to say'),
        ('blind_low_vision', 'Blind or low vision'),
        ('cognitive_autism', 'Cognitive or Autism'),
        ('cripple_mobility', 'Cripple or Mobility problem'),
        ('chronic_invisible', 'Chronic/Invisible Disability'),
        ('deaf_hearing', 'Deaf or Hearing difficulty'),
        ('mute_speaking', 'Mute or Speaking difficulty'),
        ('mental_health', 'Mental Health Condition'),
        ('other', 'Other (Please specify if you are comfortable)'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    identifier = models.CharField(max_length=20, unique=True, blank=True, help_text="Auto-generated unique identifier")
    user_group = models.CharField(max_length=20, choices=USER_GROUP_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='single')
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='other')
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, default='other')
    
    # Member Roles (Multi-select via JSON field)
    member_roles = models.JSONField(default=list, help_text="List of member roles")
    church_clergy_roles = models.JSONField(default=list, blank=True, help_text="Church/Dean clergy roles (only if clergy role is selected)")
    special_clergy_roles = models.JSONField(default=list, blank=True, help_text="Special clergy roles (only if clergy role is selected)")
    
    phone_number = models.CharField(max_length=20, unique=True)
    email_address = models.EmailField(blank=True, unique=True)
    
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
    
    # Family Details (Optional - searchable relationships)
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_father')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_mother')
    guardian = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_guardian')
    brother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='siblings_as_brother')
    sister = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='siblings_as_sister')
    uncle = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='nephews_nieces_as_uncle')
    aunt = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='nephews_nieces_as_aunt')
    friend = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='friends')
    
    # Membership Status
    membership_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS_CHOICES, default='Active')
    
    # Person with Disability (PWD)
    is_pwd = models.BooleanField(default=False, verbose_name="Person with Disability")
    pwd_type = models.CharField(max_length=50, choices=PWD_TYPE_CHOICES, blank=True, verbose_name="Type of Disability")
    pwd_other_description = models.TextField(blank=True, verbose_name="Other Disability Description")
    
    # Staff Status
    is_staff = models.BooleanField(default=False, verbose_name="Staff Member")
    
    # Hand Ordination Status
    is_ordained = models.BooleanField(default=False, verbose_name="Ordained Member")
    
    # Profile Photo
    profile_photo = models.ImageField(upload_to='member_photos/', blank=True, null=True)
    profile_photo_url = models.URLField(blank=True, help_text="Alternative to uploading a photo")
    
    # Custom Fields (JSON field for flexible custom data)
    custom_fields = models.JSONField(default=dict, blank=True, help_text="Store custom member data as key-value pairs")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    def generate_identifier(self):
        """Generate a unique identifier for the member"""
        while True:
            # Generate random 4-character segments
            segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            identifier = f"RUWE-{segment1}-{segment2}-{segment3}"
            
            # Check if this identifier already exists
            if not Member.objects.filter(identifier=identifier).exists():
                return identifier

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_identifier()
        
        # Ensure regular_member role is always present
        if 'regular_member' not in self.member_roles:
            self.member_roles.append('regular_member')
        
        super().save(*args, **kwargs)

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
    
    def has_role(self, role):
        """Check if member has a specific role"""
        return role in self.member_roles
    
    def add_role(self, role):
        """Add a role to the member"""
        if role not in self.member_roles:
            self.member_roles.append(role)
    
    def remove_role(self, role):
        """Remove a role from the member"""
        if role in self.member_roles:
            self.member_roles.remove(role)
    
    def has_clergy_role(self, clergy_role):
        """Check if member has a specific clergy role"""
        return clergy_role in self.church_clergy_roles or clergy_role in self.special_clergy_roles
    
    def add_church_clergy_role(self, role):
        """Add a church clergy role to the member"""
        if role not in self.church_clergy_roles:
            self.church_clergy_roles.append(role)
    
    def add_special_clergy_role(self, role):
        """Add a special clergy role to the member"""
        if role not in self.special_clergy_roles:
            self.special_clergy_roles.append(role)
    
    @property
    def is_clergy(self):
        """Return True if member has clergy role"""
        return 'clergy' in self.member_roles
    
    @property
    def display_roles(self):
        """Return a comma-separated list of member roles for display"""
        role_labels = []
        for role_code in self.member_roles:
            for code, label in self.MEMBER_ROLES:
                if code == role_code:
                    role_labels.append(label)
                    break
        return ', '.join(role_labels) if role_labels else 'Regular Member'
    
    @property
    def display_clergy_roles(self):
        """Return a comma-separated list of clergy roles for display"""
        clergy_labels = []
        
        # Church clergy roles
        for role_code in self.church_clergy_roles:
            for code, label in self.CHURCH_CLERGY_ROLES:
                if code == role_code:
                    clergy_labels.append(label)
                    break
        
        # Special clergy roles
        for role_code in self.special_clergy_roles:
            for code, label in self.SPECIAL_CLERGY_ROLES:
                if code == role_code:
                    clergy_labels.append(label)
                    break
        
        return ', '.join(clergy_labels) if clergy_labels else None
    
    @property
    def is_active(self):
        """Return True if member status is Active"""
        return self.membership_status == 'Active'
    
    @property
    def is_archived(self):
        """Return True if member should be archived"""
        return self.membership_status in ['Left/Quit', 'Dead']


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
