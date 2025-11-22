"""
Forms for Visitors app - Church Visitor Management System
All forms are designed to be mobile-responsive with clear validation.
"""

from django import forms
from .models import Visitor, VisitorVisit, VisitorFollowUp
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese


class VisitorForm(forms.ModelForm):
    """
    Form for adding/editing visitors.
    Most fields are optional to make data entry quick and easy.
    Only first_name, last_name, and church are required.
    """
    
    class Meta:
        model = Visitor
        fields = [
            'first_name', 'last_name', 'gender', 'age_group', 'date_of_birth',
            'marital_status', 'phone_number', 'email_address', 'physical_address',
            'city', 'country', 'church', 'is_dean_visitor', 'first_visit_date',
            'referral_source', 'invited_by_member', 'invited_by_name',
            'interested_in_membership', 'prayer_request', 'interests', 'notes'
        ]
        
        widgets = {
            # Personal Information
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name',
                'required': True
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age_group': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            
            # Contact Information
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254712345678'
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'visitor@example.com'
            }),
            'physical_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter physical address/location'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'Kenya'
            }),
            
            # Church Hierarchy
            'church': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'is_dean_visitor': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Visit Information
            'first_visit_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'referral_source': forms.Select(attrs={'class': 'form-select'}),
            'invited_by_member': forms.Select(attrs={
                'class': 'form-select'
            }),
            'invited_by_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of person who invited (if not a member)'
            }),
            
            # Interest & Engagement
            'interested_in_membership': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'prayer_request': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any prayer requests?'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ministry interests (Youth, Choir, etc.)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about this visitor'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make most fields optional except the essentials
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['church'].required = True
        
        # All other fields are optional
        for field_name in self.fields:
            if field_name not in ['first_name', 'last_name', 'church']:
                self.fields[field_name].required = False


class VisitorVisitForm(forms.ModelForm):
    """
    Form for recording subsequent visits by a visitor (2nd, 3rd visit, etc.).
    """
    
    class Meta:
        model = VisitorVisit
        fields = [
            'visit_number', 'visit_date', 'visit_type', 'service_attended',
            'came_with', 'notes'
        ]
        
        widgets = {
            'visit_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2',
                'min': '2'
            }),
            'visit_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'visit_type': forms.Select(attrs={'class': 'form-select'}),
            'service_attended': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9:00 AM Sabbath Service'
            }),
            'came_with': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Who did they come with?'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notes about this visit'
            }),
        }


class VisitorFollowUpForm(forms.ModelForm):
    """
    Form for recording follow-up attempts with visitors.
    """
    
    class Meta:
        model = VisitorFollowUp
        fields = [
            'follow_up_method', 'follow_up_date', 'status', 'purpose',
            'notes', 'next_follow_up_date'
        ]
        
        widgets = {
            'follow_up_method': forms.Select(attrs={'class': 'form-select'}),
            'follow_up_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'purpose': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Thank you for visiting'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Follow-up notes and outcome'
            }),
            'next_follow_up_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class ConvertToMemberForm(forms.Form):
    """
    Form to pre-populate member registration with visitor data.
    This helps convert a visitor to a church member.
    """
    
    # Personal Information (pre-filled from visitor)
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    gender = forms.ChoiceField(
        choices=Visitor.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Contact Information (pre-filled)
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    email_address = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    physical_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2
        })
    )
    
    # Additional member-specific fields
    confirmation_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notes about conversion to membership'
        }),
        help_text="Any additional notes about this person becoming a member"
    )
