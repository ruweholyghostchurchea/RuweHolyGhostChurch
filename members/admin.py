
from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'username', 'user_group', 'phone_number', 
        'user_home_church', 'user_home_pastorate', 'user_home_diocese', 
        'is_active', 'created_at'
    ]
    list_filter = [
        'user_group', 'user_home_diocese', 'user_home_pastorate', 
        'is_active', 'created_at', 'date_of_birth'
    ]
    search_fields = [
        'first_name', 'last_name', 'username', 'phone_number', 
        'email_address', 'baptismal_first_name', 'baptismal_last_name'
    ]
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'username', 'user_group', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email_address')
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
