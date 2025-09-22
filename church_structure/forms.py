from django import forms
from django.db.models import Q
from django.core.cache import cache
from .models import Diocese, Pastorate, Church
from members.models import Member


class DioceseForm(forms.ModelForm):
    bishop = forms.ModelChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active'
        ).order_by('first_name', 'last_name')[:100],  # Limit for performance - clergy filter removed for now
        required=False,
        empty_label="Select a bishop (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as bishop',
            'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'
        })
    )

    class Meta:
        model = Diocese
        fields = ['name', 'country', 'bishop', 'description', 'rich_description', 'established_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Diocese name'}),
            'country': forms.Select(attrs={'class': 'form-control', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (150 characters recommended)'}),
            'rich_description': forms.Textarea(attrs={'class': 'form-control rich-editor', 'rows': 10, 'placeholder': 'Detailed description with rich content...'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PastorateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cache diocese IDs for better performance
        diocese_ids = cache.get('active_diocese_ids')
        if diocese_ids is None:
            diocese_ids = list(Diocese.objects.filter(is_active=True).values_list('id', flat=True))
            cache.set('active_diocese_ids', diocese_ids, 300)  # Cache for 5 minutes
        
        # Reconstruct queryset from cached IDs
        self.fields['diocese'].queryset = Diocese.objects.filter(id__in=diocese_ids).order_by('country', 'name')
    
    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.none(),  # Will be set in __init__
        required=True,
        empty_label="Select a diocese",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'
        })
    )
    
    pastor = forms.ModelChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active'
        ).order_by('first_name', 'last_name')[:100],  # Limit for performance - clergy filter removed for now
        required=False,
        empty_label="Select a pastor (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as pastor',
            'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'
        })
    )

    class Meta:
        model = Pastorate
        fields = ['name', 'diocese', 'pastor', 'description', 'rich_description', 'established_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pastorate name', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (150 characters recommended)', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'rich_description': forms.Textarea(attrs={'class': 'form-control rich-editor', 'rows': 10, 'placeholder': 'Detailed description with rich content...', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ChurchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cache pastorate IDs for better performance
        pastorate_ids = cache.get('active_pastorate_ids')
        if pastorate_ids is None:
            pastorate_ids = list(Pastorate.objects.filter(is_active=True).values_list('id', flat=True))
            cache.set('active_pastorate_ids', pastorate_ids, 300)  # Cache for 5 minutes
        
        # Reconstruct queryset from cached IDs
        self.fields['pastorate'].queryset = Pastorate.objects.filter(id__in=pastorate_ids).select_related('diocese').order_by('diocese__name', 'name')
    
    pastorate = forms.ModelChoiceField(
        queryset=Pastorate.objects.none(),  # Will be set in __init__
        required=True,
        empty_label="Select a pastorate",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'
        })
    )
    
    head_teacher = forms.ModelChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active'
        ).order_by('first_name', 'last_name')[:100],  # Limit for performance - clergy filter removed for now
        required=False,
        empty_label="Select a head teacher (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as head teacher',
            'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'
        })
    )

    teachers = forms.ModelMultipleChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active'
        ).order_by('first_name', 'last_name')[:100],  # Limit for performance - clergy filter removed for now
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control member-multi-search',
            'data-placeholder': 'Search and select up to 12 additional teachers',
            'size': '6',
            'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'
        }),
        help_text="Hold Ctrl/Cmd to select multiple teachers (maximum 12)"
    )

    class Meta:
        model = Church
        fields = ['name', 'pastorate', 'location', 'map_link', 'phone', 'email', 'head_teacher', 'teachers', 'service_times', 'capacity', 'established_date', 'is_mission_church', 'is_diocesan_church', 'is_headquarter_church', 'is_active', 'description', 'rich_description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church name', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (city, country)', 'autocomplete': 'off', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'map_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Google Maps link (optional)', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church phone number', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Church email', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'service_times': forms.Select(attrs={'class': 'form-control', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Church capacity', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'is_mission_church': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_diocesan_church': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_headquarter_church': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (150 characters recommended)', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
            'rich_description': forms.Textarea(attrs={'class': 'form-control rich-editor', 'rows': 10, 'placeholder': 'Detailed description with rich content...', 'style': 'background: #1f2937; color: #ffffff; border: 1px solid #374151;'}),
        }

    def clean_teachers(self):
        teachers = self.cleaned_data.get('teachers')
        if teachers and teachers.count() > 12:
            raise forms.ValidationError("A church can have a maximum of 12 additional teachers.")
        return teachers

    def clean(self):
        cleaned_data = super().clean()
        is_headquarter = cleaned_data.get('is_headquarter_church')

        if is_headquarter:
            # Check if another church is already set as headquarter
            existing_headquarter = Church.objects.filter(is_headquarter_church=True)
            if self.instance.pk:
                existing_headquarter = existing_headquarter.exclude(pk=self.instance.pk)

            if existing_headquarter.exists():
                raise forms.ValidationError("There can only be one Headquarter Church. Please uncheck the existing headquarter church first.")

        return cleaned_data


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
            membership_status='Active',
            member_roles__contains=['clergy']
        ).distinct()[:20]  # Limit to 20 results for performance