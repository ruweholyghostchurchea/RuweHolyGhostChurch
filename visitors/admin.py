from django.contrib import admin
from .models import Visitor, VisitorVisit, VisitorFollowUp, VisitorStatistics


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Visitor model with comprehensive filters and display.
    """
    list_display = [
        'full_name', 'identifier', 'gender', 'age_group', 'phone_number', 'email_address',
        'church', 'pastorate', 'diocese', 'first_visit_date', 'visit_count', 
        'converted_to_member', 'is_active', 'created_at'
    ]
    
    list_filter = [
        'gender', 'age_group', 'marital_status', 'referral_source',
        'interested_in_membership', 'converted_to_member', 'is_active',
        'is_dean_visitor', 'diocese', 'pastorate', 'church',
        'first_visit_date', 'created_at'
    ]
    
    search_fields = [
        'first_name', 'last_name', 'identifier', 'phone_number', 
        'email_address', 'city', 'invited_by_name'
    ]
    
    ordering = ['-first_visit_date', '-created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('first_name', 'last_name'),
                'identifier',
                ('gender', 'age_group'),
                'date_of_birth',
                'marital_status'
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone_number',
                'email_address',
                'physical_address',
                ('city', 'country')
            )
        }),
        ('Church Visit Information', {
            'fields': (
                'church',
                'pastorate',
                'diocese',
                'is_dean_visitor',
                'first_visit_date'
            )
        }),
        ('Referral Information', {
            'fields': (
                'referral_source',
                'invited_by_member',
                'invited_by_name'
            )
        }),
        ('Interest & Engagement', {
            'fields': (
                'interested_in_membership',
                'prayer_request',
                'interests'
            )
        }),
        ('Conversion Tracking', {
            'fields': (
                'converted_to_member',
                'converted_date',
                'member_profile'
            ),
            'classes': ('collapse',)
        }),
        ('Status & Notes', {
            'fields': (
                'is_active',
                'notes'
            )
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at',
                'created_by'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['identifier', 'created_at', 'updated_at', 'pastorate', 'diocese']
    
    autocomplete_fields = ['invited_by_member', 'member_profile', 'church']
    
    def full_name(self, obj):
        """Display visitor's full name"""
        return obj.full_name
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'last_name'


@admin.register(VisitorVisit)
class VisitorVisitAdmin(admin.ModelAdmin):
    """
    Admin configuration for VisitorVisit model to track subsequent visits.
    """
    list_display = [
        'visitor', 'visit_number', 'visit_date', 'visit_type', 
        'service_attended', 'email_sent', 'created_at'
    ]
    
    list_filter = [
        'visit_type', 'visit_date', 'email_sent', 'created_at'
    ]
    
    search_fields = [
        'visitor__first_name', 'visitor__last_name', 'visitor__identifier',
        'service_attended', 'notes'
    ]
    
    ordering = ['-visit_date', '-visit_number']
    
    fieldsets = (
        ('Visit Information', {
            'fields': (
                'visitor',
                ('visit_number', 'visit_date'),
                'visit_type'
            )
        }),
        ('Attendance Details', {
            'fields': (
                'service_attended',
                'came_with',
                'notes'
            )
        }),
        ('Follow-up', {
            'fields': (
                'email_sent',
            )
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'created_by'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at']
    
    autocomplete_fields = ['visitor']


@admin.register(VisitorFollowUp)
class VisitorFollowUpAdmin(admin.ModelAdmin):
    """
    Admin configuration for VisitorFollowUp model to track follow-up attempts.
    """
    list_display = [
        'visitor', 'follow_up_method', 'follow_up_date', 'status', 
        'purpose', 'next_follow_up_date', 'created_at'
    ]
    
    list_filter = [
        'follow_up_method', 'status', 'follow_up_date', 'created_at'
    ]
    
    search_fields = [
        'visitor__first_name', 'visitor__last_name', 'visitor__identifier',
        'purpose', 'notes'
    ]
    
    ordering = ['-follow_up_date']
    
    fieldsets = (
        ('Follow-Up Information', {
            'fields': (
                'visitor',
                ('follow_up_method', 'follow_up_date'),
                'status',
                'purpose'
            )
        }),
        ('Details', {
            'fields': (
                'notes',
                'next_follow_up_date',
                'email_campaign'
            )
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at',
                'created_by'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['visitor']


@admin.register(VisitorStatistics)
class VisitorStatisticsAdmin(admin.ModelAdmin):
    """
    Admin configuration for VisitorStatistics model for reporting.
    """
    list_display = [
        'level', 'hierarchy_display', 'period_start', 'period_end',
        'total_visitors', 'first_time_visitors', 'return_visitors',
        'converted_to_members', 'generated_at'
    ]
    
    list_filter = [
        'level', 'period_start', 'period_end', 'diocese', 'pastorate', 'church'
    ]
    
    search_fields = [
        'church__name', 'pastorate__name', 'diocese__name'
    ]
    
    ordering = ['-period_end', '-generated_at']
    
    fieldsets = (
        ('Hierarchy', {
            'fields': (
                'level',
                'church',
                'pastorate',
                'diocese'
            )
        }),
        ('Period', {
            'fields': (
                ('period_start', 'period_end'),
            )
        }),
        ('Visitor Statistics', {
            'fields': (
                'total_visitors',
                'first_time_visitors',
                'return_visitors',
                'converted_to_members'
            )
        }),
        ('Demographics', {
            'fields': (
                ('male_count', 'female_count'),
                ('youth_count', 'adult_count', 'elder_count')
            )
        }),
        ('System Information', {
            'fields': (
                'generated_at',
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['generated_at']
    
    def hierarchy_display(self, obj):
        """Display the hierarchy level"""
        if obj.church:
            return f"{obj.church.name}"
        elif obj.pastorate:
            return f"{obj.pastorate.name}"
        elif obj.diocese:
            return f"{obj.diocese.name}"
        return "Dean/Headquarters"
    hierarchy_display.short_description = 'Location'
