from django import forms
from django.db.models import Q
from .models import Diocese, Pastorate, Church
from members.models import Member


class DioceseForm(forms.ModelForm):
    bishop = forms.ModelChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active',
            member_roles__contains=['clergy']
        ),
        required=False,
        empty_label="Select a bishop (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as bishop'
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
    pastor = forms.ModelChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active',
            member_roles__contains=['clergy']
        ),
        required=False,
        empty_label="Select a pastor (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as pastor'
        })
    )

    class Meta:
        model = Pastorate
        fields = ['name', 'diocese', 'pastor', 'description', 'rich_description', 'established_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pastorate name'}),
            'diocese': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (150 characters recommended)'}),
            'rich_description': forms.Textarea(attrs={'class': 'form-control rich-editor', 'rows': 10, 'placeholder': 'Detailed description with rich content...'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ChurchForm(forms.ModelForm):
    head_teacher = forms.ModelChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active',
            member_roles__contains=['clergy']
        ),
        required=False,
        empty_label="Select a head teacher (optional)",
        widget=forms.Select(attrs={
            'class': 'form-control member-search',
            'data-placeholder': 'Search and select a member as head teacher'
        })
    )

    teachers = forms.ModelMultipleChoiceField(
        queryset=Member.objects.filter(
            membership_status='Active',
            member_roles__contains=['clergy']
        ),
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
        fields = ['name', 'pastorate', 'location', 'map_link', 'phone', 'email', 'head_teacher', 'teachers', 'service_times', 'capacity', 'established_date', 'is_mission_church', 'is_diosen_church', 'is_headquarter_church', 'is_active', 'description', 'rich_description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church name'}),
            'pastorate': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (city, country)', 'autocomplete': 'off'}),
            'map_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Google Maps link (optional)'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Church email'}),
            'service_times': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Church capacity'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_mission_church': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_diosen_church': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_headquarter_church': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (150 characters recommended)'}),
            'rich_description': forms.Textarea(attrs={'class': 'form-control rich-editor', 'rows': 10, 'placeholder': 'Detailed description with rich content...'}),
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