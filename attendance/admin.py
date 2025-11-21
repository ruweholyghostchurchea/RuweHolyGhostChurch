from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord, AbsenceStreak, AttendanceStatistics


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    """
    Admin configuration for AttendanceSession model.
    """
    list_display = [
        'session_name', 'session_code', 'session_type', 'session_date', 
        'service_time', 'level', 'hierarchy_display', 'total_present', 
        'total_apology', 'total_absent', 'attendance_percentage', 
        'is_locked', 'created_at'
    ]
    
    list_filter = [
        'session_type', 'level', 'session_date', 'service_time',
        'is_dean_session', 'diocese', 'pastorate', 'church',
        'is_locked', 'is_active', 'created_at'
    ]
    
    search_fields = [
        'session_name', 'session_code', 'topic', 'location',
        'church__name', 'pastorate__name', 'diocese__name'
    ]
    
    ordering = ['-session_date', '-service_time']
    
    fieldsets = (
        ('Session Information', {
            'fields': (
                'session_name',
                'session_code',
                'session_type',
                ('session_date', 'service_time')
            )
        }),
        ('Hierarchy Level', {
            'fields': (
                'level',
                'church',
                'pastorate',
                'diocese',
                'is_dean_session'
            )
        }),
        ('Session Details', {
            'fields': (
                'location',
                'preacher',
                'topic',
                'notes'
            )
        }),
        ('Statistics (Auto-calculated)', {
            'fields': (
                ('total_expected', 'total_present'),
                ('total_apology', 'total_absent')
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': (
                'is_active',
                'is_locked'
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
    
    readonly_fields = ['session_code', 'created_at', 'updated_at']
    
    autocomplete_fields = ['church', 'preacher']
    
    def hierarchy_display(self, obj):
        """Display the hierarchy this session belongs to"""
        return obj.hierarchy_display
    hierarchy_display.short_description = 'Hierarchy'
    
    def attendance_percentage(self, obj):
        """Display attendance percentage"""
        return f"{obj.attendance_percentage}%"
    attendance_percentage.short_description = 'Attendance %'
    attendance_percentage.admin_order_field = 'total_present'


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    """
    Admin configuration for AttendanceRecord model.
    """
    list_display = [
        'member', 'session', 'status', 'check_in_time', 
        'marked_at', 'marked_by'
    ]
    
    list_filter = [
        'status', 'session__session_date', 'session__session_type',
        'session__church', 'session__pastorate', 'session__diocese',
        'marked_at'
    ]
    
    search_fields = [
        'member__first_name', 'member__last_name', 'member__identifier',
        'session__session_name', 'session__session_code', 'notes'
    ]
    
    ordering = ['-marked_at', 'member__last_name']
    
    fieldsets = (
        ('Attendance Information', {
            'fields': (
                'session',
                'member',
                'status'
            )
        }),
        ('Details', {
            'fields': (
                'check_in_time',
                'apology_reason',
                'notes'
            )
        }),
        ('System Information', {
            'fields': (
                'marked_at',
                'updated_at',
                'marked_by'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['marked_at', 'updated_at']
    
    autocomplete_fields = ['member', 'session']


@admin.register(AbsenceStreak)
class AbsenceStreakAdmin(admin.ModelAdmin):
    """
    Admin configuration for AbsenceStreak model to track consecutive absences.
    """
    list_display = [
        'member', 'church', 'current_streak', 'last_absence_date',
        'last_present_date', 'email_sent_for_3_absences', 'email_sent_date'
    ]
    
    list_filter = [
        'church', 'email_sent_for_3_absences', 'current_streak',
        'last_absence_date', 'last_present_date'
    ]
    
    search_fields = [
        'member__first_name', 'member__last_name', 'member__identifier',
        'church__name'
    ]
    
    ordering = ['-current_streak', '-last_absence_date']
    
    fieldsets = (
        ('Member & Church', {
            'fields': (
                'member',
                'church'
            )
        }),
        ('Streak Tracking', {
            'fields': (
                'current_streak',
                'last_absence_date',
                'last_present_date'
            )
        }),
        ('Email Notification', {
            'fields': (
                'email_sent_for_3_absences',
                'email_sent_date'
            )
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['member', 'church']


@admin.register(AttendanceStatistics)
class AttendanceStatisticsAdmin(admin.ModelAdmin):
    """
    Admin configuration for AttendanceStatistics model for reporting.
    """
    list_display = [
        'level', 'hierarchy_display', 'period_start', 'period_end',
        'total_sessions', 'total_attendance_records', 'total_present',
        'average_attendance_rate', 'active_members', 'inactive_members',
        'generated_at'
    ]
    
    list_filter = [
        'level', 'period_start', 'period_end', 
        'diocese', 'pastorate', 'church'
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
        ('Attendance Metrics', {
            'fields': (
                'total_sessions',
                'total_attendance_records',
                ('total_present', 'total_apology', 'total_absent'),
                'average_attendance_rate'
            )
        }),
        ('Member Engagement', {
            'fields': (
                'active_members',
                'inactive_members'
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
