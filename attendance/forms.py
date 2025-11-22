"""
Forms for Attendance app - Church Attendance/Register Management System
All forms are designed to be mobile-responsive with clear validation.
"""

from django import forms
from .models import AttendanceSession, AttendanceRecord
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese


class AttendanceSessionForm(forms.ModelForm):
    """
    Form for creating/editing attendance sessions.
    Sessions can be at Church, Pastorate, Diocese, or Dean/Headquarters level.
    """
    
    class Meta:
        model = AttendanceSession
        fields = [
            'session_name', 'session_type', 'session_date', 'service_time',
            'level', 'church', 'pastorate', 'diocese', 'is_dean_session',
            'location', 'preacher', 'topic', 'notes'
        ]
        
        widgets = {
            # Basic Information
            'session_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Sabbath Service - November 23, 2025',
                'required': True
            }),
            'session_type': forms.Select(attrs={'class': 'form-select'}),
            'session_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'service_time': forms.Select(attrs={'class': 'form-select'}),
            
            # Hierarchy Level
            'level': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'onchange': 'updateHierarchyFields()'
            }),
            'church': forms.Select(attrs={
                'class': 'form-select'
            }),
            'pastorate': forms.Select(attrs={
                'class': 'form-select'
            }),
            'diocese': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_dean_session': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Session Details
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter specific location/venue'
            }),
            'preacher': forms.Select(attrs={
                'class': 'form-select'
            }),
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sermon/teaching topic'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Session notes'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make hierarchy fields conditional based on level
        # JavaScript will handle showing/hiding the appropriate fields
        self.fields['church'].required = False
        self.fields['pastorate'].required = False
        self.fields['diocese'].required = False
    
    def clean(self):
        """
        Validate that appropriate hierarchy field is set based on level.
        """
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        church = cleaned_data.get('church')
        pastorate = cleaned_data.get('pastorate')
        diocese = cleaned_data.get('diocese')
        is_dean = cleaned_data.get('is_dean_session')
        
        # Validate hierarchy based on level
        if level == 'church' and not church:
            raise forms.ValidationError("Please select a church for church-level session.")
        elif level == 'pastorate' and not pastorate:
            raise forms.ValidationError("Please select a pastorate for pastorate-level session.")
        elif level == 'diocese' and not diocese:
            raise forms.ValidationError("Please select a diocese for diocese-level session.")
        elif level == 'dean' and not is_dean:
            cleaned_data['is_dean_session'] = True
        
        return cleaned_data


class AttendanceRecordForm(forms.ModelForm):
    """
    Form for marking individual attendance record.
    """
    
    class Meta:
        model = AttendanceRecord
        fields = ['member', 'status', 'check_in_time', 'apology_reason', 'notes']
        
        widgets = {
            'member': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'check_in_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'apology_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Reason for apology (if applicable)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            }),
        }


class BulkAttendanceForm(forms.Form):
    """
    Form for marking attendance for multiple members at once.
    Useful for quickly marking everyone as Present, then updating exceptions.
    """
    
    # Attendance status for bulk action
    bulk_status = forms.ChoiceField(
        choices=AttendanceRecord.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="Mark selected members as",
        initial='present'
    )
    
    # Members to mark (will be populated dynamically)
    member_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    def __init__(self, *args, session=None, **kwargs):
        """
        Initialize form with members from the session's hierarchy level.
        
        Args:
            session: AttendanceSession instance to get relevant members
        """
        super().__init__(*args, **kwargs)
        
        if session:
            # Get members based on session hierarchy level
            if session.church:
                # Church-level: get members from this church
                members = Member.objects.filter(user_home_church=session.church, is_active=True)
            elif session.pastorate:
                # Pastorate-level: get members from all churches in pastorate
                members = Member.objects.filter(
                    user_home_church__pastorate=session.pastorate,
                    is_active=True
                )
            elif session.diocese:
                # Diocese-level: get members from all churches in diocese
                members = Member.objects.filter(
                    user_home_church__pastorate__diocese=session.diocese,
                    is_active=True
                )
            elif session.is_dean_session:
                # Dean-level: all active members
                members = Member.objects.filter(is_active=True)
            else:
                members = Member.objects.none()
            
            # Add member selection field
            self.fields['members'] = forms.ModelMultipleChoiceField(
                queryset=members.order_by('last_name', 'first_name'),
                widget=forms.CheckboxSelectMultiple(attrs={
                    'class': 'form-check-input'
                }),
                required=False,
                label="Select Members"
            )


class SearchAttendanceForm(forms.Form):
    """
    Form for searching/filtering attendance sessions.
    """
    
    # Search by date range
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'From date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'To date'
        })
    )
    
    # Filter by session type
    session_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Session Types')] + list(AttendanceSession.SESSION_TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filter by hierarchy level
    level = forms.ChoiceField(
        required=False,
        choices=[('', 'All Levels')] + list(AttendanceSession.LEVEL_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filter by church
    church = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="All Churches"
    )
