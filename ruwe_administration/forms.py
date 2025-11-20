from django import forms
from django.forms import modelformset_factory
from .models import (
    # Church Level
    ChurchMainOffice, ChurchYouthOffice, ChurchDevelopmentOffice, 
    ChurchTravelOffice, ChurchDisciplinaryOffice,
    # Pastorate Level
    PastorateMainOffice, PastorateYouthOffice, PastorateTeachersOffice,
    # Diocese Level
    DioceseMainOffice, DioceseYouthOffice, DioceseTeachersOffice,
    # Dean Level
    DeanManagementOffice, DeanOrganizingSecretaryOffice, DeanYouthOffice,
    DeanKingsOffice, DeanArchbishopsOffice, DeanBishopsOffice, DeanPastorsOffice,
    DeanLayReadersOffice, DeanDivisionsOffice, DeanTeachersOffice, DeanWomenLeadersOffice,
    DeanEldersOffice, DeanSosoOffice, DeanCoursesOffice, DeanEcclesiasticalVestmentOffice,
    DeanEcclesiasticalCrossOffice, DeanChaplaincyOffice, DeanChurchesDataRecordsOffice,
    DeanEducationGenderEqualityOffice, DeanDevelopmentOffice, DeanDisciplinaryCommitteeOffice,
    DeanArbitrationCommitteeOffice, DeanHealthCounsellingOffice, DeanChurchesProtocolOffice,
    DeanMediaPublicityOffice
)
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese

# Helper function to get staff members
def get_staff_members_queryset():
    """Get queryset of members with staff status marked as 'Yes'"""
    return Member.objects.filter(is_staff=True).order_by('first_name', 'last_name')

# ==========================
# CHURCH LEVEL FORMS (5)
# ==========================

class ChurchMainOfficeForm(forms.ModelForm):
    class Meta:
        model = ChurchMainOffice
        fields = ['church', 'chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer', 'description']
        widgets = {
            'church': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        
        # Filter to show only staff members from the specific church
        if church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=church
            ).order_by('first_name', 'last_name')
        elif self.instance and self.instance.pk and self.instance.church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=self.instance.church
            ).order_by('first_name', 'last_name')
        else:
            staff_members = get_staff_members_queryset()
        
        for field_name in ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                          'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False

class ChurchYouthOfficeForm(forms.ModelForm):
    class Meta:
        model = ChurchYouthOffice
        fields = ['church', 'chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer', 'description']
        widgets = {
            'church': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        
        # Filter to show only staff members from the specific church
        if church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=church
            ).order_by('first_name', 'last_name')
        elif self.instance and self.instance.pk and self.instance.church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=self.instance.church
            ).order_by('first_name', 'last_name')
        else:
            staff_members = get_staff_members_queryset()
        
        for field_name in ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                          'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False

class ChurchDevelopmentOfficeForm(forms.ModelForm):
    class Meta:
        model = ChurchDevelopmentOffice
        fields = ['church', 'chairperson', 'secretary', 'treasurer', 'description']
        widgets = {
            'church': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        
        # Filter to show only staff members from the specific church
        if church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=church
            ).order_by('first_name', 'last_name')
        elif self.instance and self.instance.pk and self.instance.church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=self.instance.church
            ).order_by('first_name', 'last_name')
        else:
            staff_members = get_staff_members_queryset()
        
        for field_name in ['chairperson', 'secretary', 'treasurer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False

class ChurchTravelOfficeForm(forms.ModelForm):
    class Meta:
        model = ChurchTravelOffice
        fields = ['church', 'chairperson', 'treasurer', 'organizer', 'description']
        widgets = {
            'church': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        
        # Filter to show only staff members from the specific church
        if church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=church
            ).order_by('first_name', 'last_name')
        elif self.instance and self.instance.pk and self.instance.church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=self.instance.church
            ).order_by('first_name', 'last_name')
        else:
            staff_members = get_staff_members_queryset()
        
        for field_name in ['chairperson', 'treasurer', 'organizer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False

class ChurchDisciplinaryOfficeForm(forms.ModelForm):
    class Meta:
        model = ChurchDisciplinaryOffice
        fields = ['church', 'chairperson', 'messenger', 'members', 'description']
        widgets = {
            'church': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'messenger': forms.Select(attrs={'class': 'form-control'}),
            'members': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        
        # Filter to show only staff members from the specific church
        if church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=church
            ).order_by('first_name', 'last_name')
        elif self.instance and self.instance.pk and self.instance.church:
            staff_members = Member.objects.filter(
                is_staff=True,
                user_home_church=self.instance.church
            ).order_by('first_name', 'last_name')
        else:
            staff_members = get_staff_members_queryset()
        
        for field_name in ['chairperson', 'messenger']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False
        
        self.fields['members'].queryset = staff_members

# ==========================
# PASTORATE LEVEL FORMS (3)
# ==========================

class PastorateMainOfficeForm(forms.ModelForm):
    class Meta:
        model = PastorateMainOffice
        fields = ['pastorate', 'chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer', 
                 'church_representatives', 'description']
        widgets = {
            'pastorate': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizer': forms.Select(attrs={'class': 'form-control'}),
            'church_representatives': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        
        # Apply filtering for all position fields
        for field_name in ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                          'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False
        
        # Apply filtering for representatives
        self.fields['church_representatives'].queryset = staff_members

class PastorateYouthOfficeForm(forms.ModelForm):
    class Meta:
        model = PastorateYouthOffice
        fields = ['pastorate', 'chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer', 
                 'church_youth_representatives', 'description']
        widgets = {
            'pastorate': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizer': forms.Select(attrs={'class': 'form-control'}),
            'church_youth_representatives': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        
        # Apply filtering for all position fields
        for field_name in ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                          'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False
        
        # Apply filtering for representatives
        self.fields['church_youth_representatives'].queryset = staff_members

class PastorateTeachersOfficeForm(forms.ModelForm):
    class Meta:
        model = PastorateTeachersOffice
        fields = ['pastorate', 'chairperson', 'secretary', 'treasurer', 'organizer', 'description']
        widgets = {
            'pastorate': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are teachers (church_teacher clergy role)
        # Using JSON field filtering to check if 'church_teacher' is in church_clergy_roles
        from django.db.models import Q
        import json
        
        teacher_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['church_teacher']
        ).order_by('first_name', 'last_name')
        
        # Apply filtering for all position fields
        for field_name in ['chairperson', 'secretary', 'treasurer', 'organizer']:
            self.fields[field_name].queryset = teacher_staff_members
            self.fields[field_name].empty_label = "Select a teacher (staff member)"
            self.fields[field_name].required = False

# ==========================
# DIOCESE LEVEL FORMS (3)
# ==========================

class DioceseMainOfficeForm(forms.ModelForm):
    class Meta:
        model = DioceseMainOffice
        fields = ['diocese', 'chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer', 
                 'pastorate_representatives', 'church_representatives', 'description']
        widgets = {
            'diocese': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizer': forms.Select(attrs={'class': 'form-control'}),
            'pastorate_representatives': forms.CheckboxSelectMultiple(),
            'church_representatives': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        
        # Apply filtering for all position fields
        for field_name in ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                          'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False
        
        # Apply filtering for representatives
        self.fields['pastorate_representatives'].queryset = staff_members
        self.fields['church_representatives'].queryset = staff_members

class DioceseYouthOfficeForm(forms.ModelForm):
    class Meta:
        model = DioceseYouthOffice
        fields = ['diocese', 'chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer', 
                 'pastorate_youth_representatives', 'church_youth_representatives', 'description']
        widgets = {
            'diocese': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizer': forms.Select(attrs={'class': 'form-control'}),
            'pastorate_youth_representatives': forms.CheckboxSelectMultiple(),
            'church_youth_representatives': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        
        # Apply filtering for all position fields
        for field_name in ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                          'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
            self.fields[field_name].required = False
        
        # Apply filtering for representatives
        self.fields['pastorate_youth_representatives'].queryset = staff_members
        self.fields['church_youth_representatives'].queryset = staff_members

class DioceseTeachersOfficeForm(forms.ModelForm):
    class Meta:
        model = DioceseTeachersOffice
        fields = ['diocese', 'chairperson', 'secretary', 'treasurer', 'organizer', 'description']
        widgets = {
            'diocese': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are teachers (church_teacher clergy role)
        # Using JSON field filtering to check if 'church_teacher' is in church_clergy_roles
        teacher_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['church_teacher']
        ).order_by('first_name', 'last_name')
        
        # Apply filtering for all position fields
        for field_name in ['chairperson', 'secretary', 'treasurer', 'organizer']:
            self.fields[field_name].queryset = teacher_staff_members
            self.fields[field_name].empty_label = "Select a teacher (staff member)"
            self.fields[field_name].required = False

# ====================================
# DEAN/HEADQUARTERS LEVEL FORMS (25)
# ====================================

class DeanManagementOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanManagementOffice
        fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'internal_auditor', 'finance_records_officer',
                 'financial_advisor', 'organizing_secretary', 'assistant_organizing_secretary', 'description']
        widgets = {
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'internal_auditor': forms.Select(attrs={'class': 'form-control'}),
            'finance_records_officer': forms.Select(attrs={'class': 'form-control'}),
            'financial_advisor': forms.Select(attrs={'class': 'form-control'}),
            'organizing_secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizing_secretary': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                          'treasurer', 'assistant_treasurer', 'internal_auditor', 'finance_records_officer',
                          'financial_advisor', 'organizing_secretary', 'assistant_organizing_secretary']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"

class DeanOrganizingSecretaryOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanOrganizingSecretaryOffice
        fields = ['officers', 'description']
        widgets = {
            'officers': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        self.fields['officers'].queryset = get_staff_members_queryset()

class DeanYouthOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanYouthOffice
        fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                 'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer',
                 'diocese_youth_representatives', 'pastorate_youth_representatives', 
                 'church_youth_representatives', 'description']
        widgets = {
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_organizer': forms.Select(attrs={'class': 'form-control'}),
            'diocese_youth_representatives': forms.CheckboxSelectMultiple(),
            'pastorate_youth_representatives': forms.CheckboxSelectMultiple(),
            'church_youth_representatives': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class DeanKingsOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanKingsOffice
        fields = ['advisers', 'aides', 'description']
        widgets = {
            'advisers': forms.CheckboxSelectMultiple(),
            'aides': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class DeanArchbishopsOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanArchbishopsOffice
        fields = ['advisers', 'aides', 'woman_aide', 'description']
        widgets = {
            'advisers': forms.CheckboxSelectMultiple(),
            'aides': forms.CheckboxSelectMultiple(),
            'woman_aide': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        self.fields['advisers'].queryset = staff_members
        self.fields['aides'].queryset = staff_members
        self.fields['woman_aide'].queryset = staff_members.filter(gender='Female')
        self.fields['woman_aide'].empty_label = "Select a female staff member"

# Common form pattern for Dean offices with standard positions
class DeanStandardOfficeForm(forms.ModelForm):
    """Base form for Dean offices with standard positions"""
    class Meta:
        fields = ['head', 'assistant_head', 'chairman', 'assistant_chair', 
                 'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'chairman': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chair': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'organizing_secretary': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'chairman', 'assistant_chair',
                          'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']:
            if field_name in self.fields:
                self.fields[field_name].queryset = staff_members
                self.fields[field_name].empty_label = "Select a staff member"

class DeanBishopsOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanBishopsOffice
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are bishops
        bishop_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['diocese_bishop']
        ).order_by('first_name', 'last_name')
        
        for field_name in ['head', 'assistant_head', 'chairman', 'assistant_chair',
                          'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']:
            if field_name in self.fields:
                self.fields[field_name].queryset = bishop_staff_members
                self.fields[field_name].empty_label = "Select a bishop (staff member)"

class DeanPastorsOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanPastorsOffice
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are pastors
        pastor_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['pastorate_pastor']
        ).order_by('first_name', 'last_name')
        
        for field_name in ['head', 'assistant_head', 'chairman', 'assistant_chair',
                          'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']:
            if field_name in self.fields:
                self.fields[field_name].queryset = pastor_staff_members
                self.fields[field_name].empty_label = "Select a pastor (staff member)"

class DeanLayReadersOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanLayReadersOffice
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are lay readers
        lay_reader_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['pastorate_lay_reader']
        ).order_by('first_name', 'last_name')
        
        for field_name in ['head', 'assistant_head', 'chairman', 'assistant_chair',
                          'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']:
            if field_name in self.fields:
                self.fields[field_name].queryset = lay_reader_staff_members
                self.fields[field_name].empty_label = "Select a lay reader (staff member)"

class DeanDivisionsOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanDivisionsOffice
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are divisions
        division_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['pastorate_division']
        ).order_by('first_name', 'last_name')
        
        for field_name in ['head', 'assistant_head', 'chairman', 'assistant_chair',
                          'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']:
            if field_name in self.fields:
                self.fields[field_name].queryset = division_staff_members
                self.fields[field_name].empty_label = "Select a division (staff member)"

class DeanTeachersOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanTeachersOffice
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are teachers
        teacher_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['church_teacher']
        ).order_by('first_name', 'last_name')
        
        for field_name in ['head', 'assistant_head', 'chairman', 'assistant_chair',
                          'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']:
            if field_name in self.fields:
                self.fields[field_name].queryset = teacher_staff_members
                self.fields[field_name].empty_label = "Select a teacher (staff member)"

class DeanWomenLeadersOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanWomenLeadersOffice
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members who are women leaders
        woman_leader_staff_members = Member.objects.filter(
            is_staff=True,
            church_clergy_roles__contains=['pastorate_woman_leader']
        ).order_by('first_name', 'last_name')
        
        for field_name in ['head', 'assistant_head', 'chairman', 'assistant_chair',
                          'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']:
            if field_name in self.fields:
                self.fields[field_name].queryset = woman_leader_staff_members
                self.fields[field_name].empty_label = "Select a woman leader (staff member)"

class DeanEldersOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanEldersOffice

class DeanSosoOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanSosoOffice

# Specialized Dean Office Forms

class DeanCoursesOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanCoursesOffice
        fields = ['head', 'assistant_head', 'secretary', 'assistant_secretary', 'treasurer', 
                 'assistant_treasurer', 'communication_officer', 'male_officer', 'female_officer', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'assistant_treasurer': forms.Select(attrs={'class': 'form-control'}),
            'communication_officer': forms.Select(attrs={'class': 'form-control'}),
            'male_officer': forms.Select(attrs={'class': 'form-control'}),
            'female_officer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'secretary', 'assistant_secretary', 'treasurer', 
                          'assistant_treasurer', 'communication_officer', 'male_officer', 'female_officer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"

class DeanEcclesiasticalVestmentOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanEcclesiasticalVestmentOffice
        fields = ['head', 'assistant_head', 'secretary', 'treasurer', 'embroiderer',
                 'male_tailors', 'female_tailors', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'embroiderer': forms.Select(attrs={'class': 'form-control'}),
            'male_tailors': forms.CheckboxSelectMultiple(),
            'female_tailors': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'secretary', 'treasurer', 'embroiderer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
        self.fields['male_tailors'].queryset = staff_members
        self.fields['female_tailors'].queryset = staff_members

class DeanEcclesiasticalCrossOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanEcclesiasticalCrossOffice
        fields = ['head', 'secretary', 'treasurer', 'main_woodworker', 'woodworkers', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'treasurer': forms.Select(attrs={'class': 'form-control'}),
            'main_woodworker': forms.Select(attrs={'class': 'form-control'}),
            'woodworkers': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'secretary', 'treasurer', 'main_woodworker']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
        self.fields['woodworkers'].queryset = staff_members

class DeanChaplaincyOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanChaplaincyOffice
        fields = ['head', 'assistant_head', 'officers', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'officers': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
        self.fields['officers'].queryset = staff_members

class DeanChurchesDataRecordsOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanChurchesDataRecordsOffice
        fields = ['head', 'secretary', 'officers', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'officers': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'secretary']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
        self.fields['officers'].queryset = staff_members

class DeanEducationGenderEqualityOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanEducationGenderEqualityOffice
        fields = ['head', 'assistant_head', 'secretary', 'officers', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'officers': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'secretary']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
        self.fields['officers'].queryset = staff_members

class DeanDevelopmentOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanDevelopmentOffice
        fields = ['head', 'assistant_head', 'officers', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'officers': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"
        self.fields['officers'].queryset = staff_members

class DeanDisciplinaryCommitteeOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanDisciplinaryCommitteeOffice
        fields = ['head', 'assistant_head', 'secretary', 'assistant_secretary', 'messenger', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'assistant_secretary': forms.Select(attrs={'class': 'form-control'}),
            'messenger': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'secretary', 'assistant_secretary', 'messenger']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"

class DeanArbitrationCommitteeOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanArbitrationCommitteeOffice
        fields = ['head', 'assistant_head', 'chairperson', 'assistant_chairperson', 'secretary', 
                 'women_leader', 'messenger', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'chairperson': forms.Select(attrs={'class': 'form-control'}),
            'assistant_chairperson': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'women_leader': forms.Select(attrs={'class': 'form-control'}),
            'messenger': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'chairperson', 'assistant_chairperson', 
                          'secretary', 'women_leader', 'messenger']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"

class DeanHealthCounsellingOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanHealthCounsellingOffice
        fields = ['head', 'assistant_head', 'secretary', 'male_officer', 'female_officer', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'male_officer': forms.Select(attrs={'class': 'form-control'}),
            'female_officer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'secretary', 'male_officer', 'female_officer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"

class DeanChurchesProtocolOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanChurchesProtocolOffice
        fields = ['head', 'assistant_head', 'secretary', 'male_officer', 'female_officer', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'secretary': forms.Select(attrs={'class': 'form-control'}),
            'male_officer': forms.Select(attrs={'class': 'form-control'}),
            'female_officer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'secretary', 'male_officer', 'female_officer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"

class DeanMediaPublicityOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanMediaPublicityOffice
        fields = ['head', 'assistant_head', 'designer', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'}),
            'assistant_head': forms.Select(attrs={'class': 'form-control'}),
            'designer': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only staff members
        staff_members = get_staff_members_queryset()
        for field_name in ['head', 'assistant_head', 'designer']:
            self.fields[field_name].queryset = staff_members
            self.fields[field_name].empty_label = "Select a staff member"