
from django.contrib import admin
from .models import Member, MemberDocument

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'username', 'user_group', 'gender', 'marital_status',
        'location', 'phone_number', 'membership_status', 'is_staff', 'is_ordained', 
        'is_pwd', 'user_home_church', 'user_home_pastorate', 'user_home_diocese', 'created_at'
    ]
    list_filter = [
        'user_group', 'gender', 'marital_status', 'location', 'education_level',
        'membership_status', 'is_staff', 'is_ordained', 'is_pwd',
        'user_home_diocese', 'user_home_pastorate', 'created_at', 'date_of_birth'
    ]
    search_fields = [
        'first_name', 'last_name', 'username', 'phone_number', 
        'email_address', 'baptismal_first_name', 'baptismal_last_name'
    ]
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'username', 'user_group', 'gender', 
                      'date_of_birth', 'marital_status', 'location', 'education_level')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email_address')
        }),
        ('Status Information', {
            'fields': ('membership_status', 'is_staff', 'is_ordained')
        }),
        ('Person with Disability (PWD)', {
            'fields': ('is_pwd', 'pwd_type', 'pwd_other_description'),
            'classes': ('collapse',),
        }),
        ('Family Details', {
            'fields': ('father', 'mother', 'guardian', 'brother', 'sister', 'uncle', 'aunt', 'friend'),
            'classes': ('collapse',),
        }),
        ('Job Information', {
            'fields': ('job_occupation_income',)
        }),
        ('Baptismal Information', {
            'fields': ('baptismal_first_name', 'baptismal_last_name', 'date_baptized', 'date_joined_religion')
        }),
        ('Home Church Structure', {
            'fields': ('user_home_diocese', 'user_home_pastorate', 'user_home_church')
        }),
        ('Town Church Structure (Optional)', {
            'fields': ('user_town_diocese', 'user_town_pastorate', 'user_town_church'),
            'classes': ('collapse',)
        }),
        ('Emergency Contacts', {
            'fields': (
                ('emergency_contact_1_name', 'emergency_contact_1_relationship'),
                ('emergency_contact_1_phone', 'emergency_contact_1_email'),
                ('emergency_contact_2_name', 'emergency_contact_2_relationship'),
                ('emergency_contact_2_phone', 'emergency_contact_2_email'),
            ),
            'classes': ('collapse',)
        }),
        ('Profile & Media', {
            'fields': ('profile_photo', 'profile_photo_url'),
            'classes': ('collapse',)
        }),
        ('Custom Fields', {
            'fields': ('custom_fields',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('is_active', 'date_joined_app'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['date_joined_app']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'last_name'


@admin.register(MemberDocument)
class MemberDocumentAdmin(admin.ModelAdmin):
    list_display = ['member', 'title', 'document_type', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['member__first_name', 'member__last_name', 'title', 'description']
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('member', 'document_type', 'title', 'description')
        }),
        ('File Upload', {
            'fields': ('document_file', 'uploaded_by')
        }),
    )
    
    readonly_fields = ['uploaded_at']
