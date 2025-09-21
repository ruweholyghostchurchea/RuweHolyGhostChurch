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

class DeanOrganizingSecretaryOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanOrganizingSecretaryOffice
        fields = ['officers', 'description']
        widgets = {
            'officers': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

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

class DeanBishopsOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanBishopsOffice

class DeanPastorsOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanPastorsOffice

class DeanLayReadersOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanLayReadersOffice

class DeanDivisionsOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanDivisionsOffice

class DeanTeachersOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanTeachersOffice

class DeanWomenLeadersOfficeForm(DeanStandardOfficeForm):
    class Meta(DeanStandardOfficeForm.Meta):
        model = DeanWomenLeadersOffice

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

class DeanArbitrationCommitteeOfficeForm(forms.ModelForm):
    class Meta:
        model = DeanArbitrationCommitteeOffice
        fields = ['head', 'assistant_head', 'chairperson', 'assistant_chairperson',
                 'secretary', 'women_leader', 'messenger', 'description']
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