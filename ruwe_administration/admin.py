from django.contrib import admin
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

# =========================
# BASE ADMIN CONFIGURATION
# =========================

class BaseAdministrationAdmin(admin.ModelAdmin):
    """Base admin configuration for all administration offices"""
    list_display = ['name', 'identifier', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'identifier', 'description']
    ordering = ['-created_at']
    readonly_fields = ['identifier', 'slug', 'created_at', 'updated_at']

# =========================
# CHURCH LEVEL ADMIN (5)
# =========================

@admin.register(ChurchMainOffice)
class ChurchMainOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'church', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['church__pastorate__diocese', 'church__pastorate', 'church', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'church__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(ChurchYouthOffice)
class ChurchYouthOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'church', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['church__pastorate__diocese', 'church__pastorate', 'church', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'church__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(ChurchDevelopmentOffice)
class ChurchDevelopmentOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'church', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['church__pastorate__diocese', 'church__pastorate', 'church', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'church__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'secretary', 'treasurer']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(ChurchTravelOffice)
class ChurchTravelOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'church', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['church__pastorate__diocese', 'church__pastorate', 'church', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'church__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'treasurer', 'organizer']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(ChurchDisciplinaryOffice)
class ChurchDisciplinaryOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'church', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['church__pastorate__diocese', 'church__pastorate', 'church', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'church__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'messenger']
    filter_horizontal = ['members']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

# =========================
# PASTORATE LEVEL ADMIN (3)
# =========================

@admin.register(PastorateMainOffice)
class PastorateMainOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'pastorate', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['pastorate__diocese', 'pastorate', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'pastorate__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']
    filter_horizontal = ['church_representatives']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(PastorateYouthOffice)
class PastorateYouthOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'pastorate', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['pastorate__diocese', 'pastorate', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'pastorate__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']
    filter_horizontal = ['church_youth_representatives']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(PastorateTeachersOffice)
class PastorateTeachersOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'pastorate', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['pastorate__diocese', 'pastorate', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'pastorate__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'secretary', 'treasurer', 'organizer']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

# =========================
# DIOCESE LEVEL ADMIN (3)
# =========================

@admin.register(DioceseMainOffice)
class DioceseMainOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'diocese', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['diocese', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'diocese__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']
    filter_horizontal = ['pastorate_representatives', 'church_representatives']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(DioceseYouthOffice)
class DioceseYouthOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'diocese', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['diocese', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'diocese__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']
    filter_horizontal = ['pastorate_youth_representatives', 'church_youth_representatives']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(DioceseTeachersOffice)
class DioceseTeachersOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'diocese', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    list_filter = ['diocese', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'diocese__name', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'secretary', 'treasurer', 'organizer']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

# ====================================
# DEAN/HEADQUARTERS LEVEL ADMIN (25)
# ====================================

@admin.register(DeanManagementOffice)
class DeanManagementOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'internal_auditor', 'finance_records_officer',
                     'financial_advisor', 'organizing_secretary', 'assistant_organizing_secretary']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(DeanOrganizingSecretaryOffice)
class DeanOrganizingSecretaryOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'officers_count', 'identifier', 'is_active', 'created_at']
    filter_horizontal = ['officers']
    
    def officers_count(self, obj):
        return obj.officers.count()
    officers_count.short_description = 'Officers Count'

@admin.register(DeanYouthOffice)
class DeanYouthOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'chairperson__first_name', 'chairperson__last_name']
    raw_id_fields = ['chairperson', 'assistant_chairperson', 'secretary', 'assistant_secretary',
                     'treasurer', 'assistant_treasurer', 'organizer', 'assistant_organizer']
    filter_horizontal = ['diocese_youth_representatives', 'pastorate_youth_representatives', 'church_youth_representatives']
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(DeanKingsOffice)
class DeanKingsOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'advisers_count', 'aides_count', 'identifier', 'is_active', 'created_at']
    filter_horizontal = ['advisers', 'aides']
    
    def advisers_count(self, obj):
        return obj.advisers.count()
    advisers_count.short_description = 'Advisers Count'
    
    def aides_count(self, obj):
        return obj.aides.count()
    aides_count.short_description = 'Aides Count'

@admin.register(DeanArchbishopsOffice)
class DeanArchbishopsOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'advisers_count', 'aides_count', 'woman_aide_name', 'identifier', 'is_active', 'created_at']
    filter_horizontal = ['advisers', 'aides']
    raw_id_fields = ['woman_aide']
    
    def advisers_count(self, obj):
        return obj.advisers.count()
    advisers_count.short_description = 'Advisers Count'
    
    def aides_count(self, obj):
        return obj.aides.count()
    aides_count.short_description = 'Aides Count'
    
    def woman_aide_name(self, obj):
        return obj.woman_aide.full_name if obj.woman_aide else "Not Assigned"
    woman_aide_name.short_description = 'Woman Aide'

# Common admin class for Dean offices with standard structure
class DeanStandardOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'chairman', 'assistant_chair', 
                     'secretary', 'assistant_secretary', 'treasurer', 'organizing_secretary']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'

@admin.register(DeanBishopsOffice)
class DeanBishopsOfficeAdmin(DeanStandardOfficeAdmin):
    pass

@admin.register(DeanPastorsOffice)
class DeanPastorsOfficeAdmin(DeanStandardOfficeAdmin):
    pass

@admin.register(DeanLayReadersOffice)
class DeanLayReadersOfficeAdmin(DeanStandardOfficeAdmin):
    pass

@admin.register(DeanDivisionsOffice)
class DeanDivisionsOfficeAdmin(DeanStandardOfficeAdmin):
    pass

@admin.register(DeanTeachersOffice)
class DeanTeachersOfficeAdmin(DeanStandardOfficeAdmin):
    pass

@admin.register(DeanWomenLeadersOffice)
class DeanWomenLeadersOfficeAdmin(DeanStandardOfficeAdmin):
    pass

@admin.register(DeanEldersOffice)
class DeanEldersOfficeAdmin(DeanStandardOfficeAdmin):
    pass

@admin.register(DeanSosoOffice)
class DeanSosoOfficeAdmin(DeanStandardOfficeAdmin):
    pass

# Specialized Dean office admins

@admin.register(DeanCoursesOffice)
class DeanCoursesOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'secretary', 'assistant_secretary', 'treasurer', 
                     'assistant_treasurer', 'communication_officer', 'male_officer', 'female_officer']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'

@admin.register(DeanEcclesiasticalVestmentOffice)
class DeanEcclesiasticalVestmentOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'male_tailors_count', 'female_tailors_count', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'secretary', 'treasurer', 'embroiderer']
    filter_horizontal = ['male_tailors', 'female_tailors']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def male_tailors_count(self, obj):
        return obj.male_tailors.count()
    male_tailors_count.short_description = 'Male Tailors'
    
    def female_tailors_count(self, obj):
        return obj.female_tailors.count()
    female_tailors_count.short_description = 'Female Tailors'

@admin.register(DeanEcclesiasticalCrossOffice)
class DeanEcclesiasticalCrossOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'woodworkers_count', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'secretary', 'treasurer', 'main_woodworker']
    filter_horizontal = ['woodworkers']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def woodworkers_count(self, obj):
        return obj.woodworkers.count()
    woodworkers_count.short_description = 'Woodworkers Count'

@admin.register(DeanChaplaincyOffice)
class DeanChaplaincyOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'officers_count', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head']
    filter_horizontal = ['officers']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def officers_count(self, obj):
        return obj.officers.count()
    officers_count.short_description = 'Officers Count'

@admin.register(DeanChurchesDataRecordsOffice)
class DeanChurchesDataRecordsOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'officers_count', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'secretary']
    filter_horizontal = ['officers']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def officers_count(self, obj):
        return obj.officers.count()
    officers_count.short_description = 'Officers Count'

@admin.register(DeanEducationGenderEqualityOffice)
class DeanEducationGenderEqualityOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'officers_count', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'secretary']
    filter_horizontal = ['officers']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def officers_count(self, obj):
        return obj.officers.count()
    officers_count.short_description = 'Officers Count'

@admin.register(DeanDevelopmentOffice)
class DeanDevelopmentOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'officers_count', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head']
    filter_horizontal = ['officers']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def officers_count(self, obj):
        return obj.officers.count()
    officers_count.short_description = 'Officers Count'

@admin.register(DeanDisciplinaryCommitteeOffice)
class DeanDisciplinaryCommitteeOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'secretary', 'assistant_secretary', 'messenger']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'

@admin.register(DeanArbitrationCommitteeOffice)
class DeanArbitrationCommitteeOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'chairperson_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'chairperson', 'assistant_chairperson',
                     'secretary', 'women_leader', 'messenger']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def chairperson_name(self, obj):
        return obj.chairperson.full_name if obj.chairperson else "Not Assigned"
    chairperson_name.short_description = 'Chairperson'

@admin.register(DeanHealthCounsellingOffice)
class DeanHealthCounsellingOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'secretary', 'male_officer', 'female_officer']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'

@admin.register(DeanChurchesProtocolOffice)
class DeanChurchesProtocolOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'secretary', 'male_officer', 'female_officer']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'

@admin.register(DeanMediaPublicityOffice)
class DeanMediaPublicityOfficeAdmin(BaseAdministrationAdmin):
    list_display = ['name', 'head_name', 'designer_name', 'identifier', 'is_active', 'created_at']
    search_fields = ['name', 'identifier', 'head__first_name', 'head__last_name']
    raw_id_fields = ['head', 'assistant_head', 'designer']
    
    def head_name(self, obj):
        return obj.head.full_name if obj.head else "Not Assigned"
    head_name.short_description = 'Head'
    
    def designer_name(self, obj):
        return obj.designer.full_name if obj.designer else "Not Assigned"
    designer_name.short_description = 'Designer'