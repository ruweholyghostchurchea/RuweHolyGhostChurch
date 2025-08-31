
from django import forms
from django.db.models import Q
from .models import Diocese, Pastorate, Church
from members.models import Member


class DioceseForm(forms.ModelForm):
    bishop = forms.ModelChoiceField(
        queryset=Member.objects.filter(membership_status='Active'),
        required=False,
        empty_label="Select a bishop (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as bishop'
        })
    )
    
    class Meta:
        model = Diocese
        fields = ['name', 'country', 'bishop', 'description', 'established_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Diocese name'}),
            'country': forms.Select(attrs={'class': 'form-control', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PastorateForm(forms.ModelForm):
    pastor = forms.ModelChoiceField(
        queryset=Member.objects.filter(membership_status='Active'),
        required=False,
        empty_label="Select a pastor (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as pastor'
        })
    )
    
    class Meta:
        model = Pastorate
        fields = ['name', 'diocese', 'pastor', 'description', 'established_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pastorate name'}),
            'diocese': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ChurchForm(forms.ModelForm):
    head_teacher = forms.ModelChoiceField(
        queryset=Member.objects.filter(membership_status='Active'),
        required=False,
        empty_label="Select a head teacher (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as head teacher'
        })
    )
    
    teachers = forms.ModelMultipleChoiceField(
        queryset=Member.objects.filter(membership_status='Active'),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control member-multi-search',
            'data-placeholder': 'Search and select up to 12 additional teachers',
            'size': '6'
        }),
        help_text="Hold Ctrl/Cmd to select multiple teachers (maximum 12)"
    )
    
    class Meta:
        model = Church
        fields = ['name', 'pastorate', 'address', 'phone', 'email', 'head_teacher', 'teachers', 'service_times', 'capacity', 'established_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church name'}),
            'pastorate': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Church address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Church email'}),
            'service_times': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Service schedule information'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Church capacity'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_teachers(self):
        teachers = self.cleaned_data.get('teachers')
        if teachers and teachers.count() > 12:
            raise forms.ValidationError("A church can have a maximum of 12 additional teachers.")
        return teachers


class MemberSearchForm(forms.Form):
    """Form for AJAX member search"""
    search = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search members by name, username, or phone...'
        })
    )
    
    def search_members(self):
        search_term = self.cleaned_data.get('search', '')
        if len(search_term) < 2:
            return Member.objects.none()
        
        return Member.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(username__icontains=search_term) |
            Q(phone_number__icontains=search_term),
            membership_status='Active'
        ).distinct()[:20]  # Limit to 20 results for performance
