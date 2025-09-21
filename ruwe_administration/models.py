from django.db import models
from django.utils.text import slugify
from members.models import Member
from church_structure.models import Church, Pastorate, Diocese
import random
import string

class BaseAdministrationOffice(models.Model):
    """Base model for all administration offices"""
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=20, unique=True, blank=True, help_text="Auto-generated unique identifier")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Office description and responsibilities")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def generate_identifier(self):
        """Generate unique identifier for the office"""
        prefix = self.__class__.__name__[:3].upper()
        while True:
            suffix = ''.join(random.choices(string.digits, k=4))
            identifier = f"{prefix}{suffix}"
            if not self.__class__.objects.filter(identifier=identifier).exists():
                return identifier

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_identifier()
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.identifier}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.identifier})"


# =========================
# CHURCH LEVEL OFFICES (5)
# =========================

class ChurchMainOffice(BaseAdministrationOffice):
    """Church Main Office - Runs most Church activities"""
    church = models.OneToOneField(Church, on_delete=models.CASCADE, related_name='main_office')
    
    # Main positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_assistant_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_organizer')
    assistant_organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_main_assistant_organizer')

    class Meta:
        verbose_name = "Church Main Office"
        verbose_name_plural = "Church Main Offices"

class ChurchYouthOffice(BaseAdministrationOffice):
    """Church Youth Office - Central hub for youth activities"""
    church = models.OneToOneField(Church, on_delete=models.CASCADE, related_name='youth_office')
    
    # Youth positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_assistant_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_organizer')
    assistant_organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_youth_assistant_organizer')

    class Meta:
        verbose_name = "Church Youth Office"
        verbose_name_plural = "Church Youth Offices"

class ChurchDevelopmentOffice(BaseAdministrationOffice):
    """Church Development Office - Plans development fundraising"""
    church = models.OneToOneField(Church, on_delete=models.CASCADE, related_name='development_office')
    
    # Development positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_development_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_development_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_development_treasurer')

    class Meta:
        verbose_name = "Church Development Office"
        verbose_name_plural = "Church Development Offices"

class ChurchTravelOffice(BaseAdministrationOffice):
    """Church Travel Office - Plans and facilitates church travel"""
    church = models.OneToOneField(Church, on_delete=models.CASCADE, related_name='travel_office')
    
    # Travel positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_travel_chairperson')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_travel_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_travel_organizer')

    class Meta:
        verbose_name = "Church Travel Office"
        verbose_name_plural = "Church Travel Offices"

class ChurchDisciplinaryOffice(BaseAdministrationOffice):
    """Church Disciplinary Office - Enforces Church Canon Law"""
    church = models.OneToOneField(Church, on_delete=models.CASCADE, related_name='disciplinary_office')
    
    # Disciplinary positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_disciplinary_chairperson')
    messenger = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='church_disciplinary_messenger')
    members = models.ManyToManyField(Member, blank=True, related_name='church_disciplinary_members')

    class Meta:
        verbose_name = "Church Disciplinary Office"
        verbose_name_plural = "Church Disciplinary Offices"


# =========================
# PASTORATE LEVEL OFFICES (3)
# =========================

class PastorateMainOffice(BaseAdministrationOffice):
    """Pastorate Main Office - Runs most Pastorate activities"""
    pastorate = models.OneToOneField(Pastorate, on_delete=models.CASCADE, related_name='main_office')
    
    # Main positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_assistant_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_organizer')
    assistant_organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_main_assistant_organizer')
    church_representatives = models.ManyToManyField(Member, blank=True, related_name='pastorate_main_church_representatives')

    class Meta:
        verbose_name = "Pastorate Main Office"
        verbose_name_plural = "Pastorate Main Offices"

class PastorateYouthOffice(BaseAdministrationOffice):
    """Pastorate Youth Office - Central hub for pastorate youth activities"""
    pastorate = models.OneToOneField(Pastorate, on_delete=models.CASCADE, related_name='youth_office')
    
    # Youth positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_assistant_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_organizer')
    assistant_organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_youth_assistant_organizer')
    church_youth_representatives = models.ManyToManyField(Member, blank=True, related_name='pastorate_youth_church_representatives')

    class Meta:
        verbose_name = "Pastorate Youth Office"
        verbose_name_plural = "Pastorate Youth Offices"

class PastorateTeachersOffice(BaseAdministrationOffice):
    """Pastorate Teachers Office - All teachers from different Churches within Pastorate"""
    pastorate = models.OneToOneField(Pastorate, on_delete=models.CASCADE, related_name='teachers_office')
    
    # Teachers positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_teachers_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_teachers_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_teachers_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorate_teachers_organizer')

    class Meta:
        verbose_name = "Pastorate Teachers Office"
        verbose_name_plural = "Pastorate Teachers Offices"


# =========================
# DIOCESE LEVEL OFFICES (3)
# =========================

class DioceseMainOffice(BaseAdministrationOffice):
    """Diocese Main Office - Runs most Diocese activities"""
    diocese = models.OneToOneField(Diocese, on_delete=models.CASCADE, related_name='main_office')
    
    # Main positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_assistant_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_organizer')
    assistant_organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_main_assistant_organizer')
    pastorate_representatives = models.ManyToManyField(Member, blank=True, related_name='diocese_main_pastorate_representatives')
    church_representatives = models.ManyToManyField(Member, blank=True, related_name='diocese_main_church_representatives')

    class Meta:
        verbose_name = "Diocese Main Office"
        verbose_name_plural = "Diocese Main Offices"

class DioceseYouthOffice(BaseAdministrationOffice):
    """Diocese Youth Office - Central hub for diocese youth activities"""
    diocese = models.OneToOneField(Diocese, on_delete=models.CASCADE, related_name='youth_office')
    
    # Youth positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_assistant_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_organizer')
    assistant_organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_youth_assistant_organizer')
    pastorate_youth_representatives = models.ManyToManyField(Member, blank=True, related_name='diocese_youth_pastorate_representatives')
    church_youth_representatives = models.ManyToManyField(Member, blank=True, related_name='diocese_youth_church_representatives')

    class Meta:
        verbose_name = "Diocese Youth Office"
        verbose_name_plural = "Diocese Youth Offices"

class DioceseTeachersOffice(BaseAdministrationOffice):
    """Diocese Teachers Office - All teachers of different Churches from Pastorates within Diocese"""
    diocese = models.OneToOneField(Diocese, on_delete=models.CASCADE, related_name='teachers_office')
    
    # Teachers positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_teachers_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_teachers_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_teachers_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='diocese_teachers_organizer')

    class Meta:
        verbose_name = "Diocese Teachers Office"
        verbose_name_plural = "Diocese Teachers Offices"


# ====================================
# DEAN/HEADQUARTERS LEVEL OFFICES (25)
# ====================================

# 1. Dean Management/Executive Office
class DeanManagementOffice(BaseAdministrationOffice):
    """Dean Management/Executive Office"""
    name = models.CharField(max_length=200, default="Dean Management Office")
    
    # Management positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_assistant_treasurer')
    internal_auditor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_internal_auditor')
    finance_records_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_finance_records_officer')
    financial_advisor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_financial_advisor')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_organizing_secretary')
    assistant_organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_assistant_organizing_secretary')

    class Meta:
        verbose_name = "Dean Management Office"
        verbose_name_plural = "Dean Management Offices"

# 2. Dean Organising Secretary Office
class DeanOrganizingSecretaryOffice(BaseAdministrationOffice):
    """Dean Organising Secretary Office - Officers working under Organizing Secretary"""
    name = models.CharField(max_length=200, default="Dean Organizing Secretary Office")
    
    # Officers (up to 10)
    officers = models.ManyToManyField(Member, blank=True, related_name='dean_organizing_secretary_officers')

    class Meta:
        verbose_name = "Dean Organizing Secretary Office"
        verbose_name_plural = "Dean Organizing Secretary Offices"

# 3. Dean Youth Office
class DeanYouthOffice(BaseAdministrationOffice):
    """Dean Youth Office - Central hub for dean youth activities"""
    name = models.CharField(max_length=200, default="Dean Youth Office")
    
    # Youth positions
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_assistant_treasurer')
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_organizer')
    assistant_organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_youth_assistant_organizer')
    diocese_youth_representatives = models.ManyToManyField(Member, blank=True, related_name='dean_youth_diocese_representatives')
    pastorate_youth_representatives = models.ManyToManyField(Member, blank=True, related_name='dean_youth_pastorate_representatives')
    church_youth_representatives = models.ManyToManyField(Member, blank=True, related_name='dean_youth_church_representatives')

    class Meta:
        verbose_name = "Dean Youth Office"
        verbose_name_plural = "Dean Youth Offices"

# 4. Dean King's Office
class DeanKingsOffice(BaseAdministrationOffice):
    """Dean King's Office"""
    name = models.CharField(max_length=200, default="Dean King's Office")
    
    # King's positions
    advisers = models.ManyToManyField(Member, blank=True, related_name='dean_king_advisers')  # 10 advisers
    aides = models.ManyToManyField(Member, blank=True, related_name='dean_king_aides')  # 3 aides

    class Meta:
        verbose_name = "Dean King's Office"
        verbose_name_plural = "Dean King's Offices"

# 5. Dean Archbishop's Office
class DeanArchbishopsOffice(BaseAdministrationOffice):
    """Dean Archbishop's Office"""
    name = models.CharField(max_length=200, default="Dean Archbishop's Office")
    
    # Archbishop's positions
    advisers = models.ManyToManyField(Member, blank=True, related_name='dean_archbishop_advisers')  # 15 advisers
    aides = models.ManyToManyField(Member, blank=True, related_name='dean_archbishop_aides')  # 5 aides
    woman_aide = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_archbishop_woman_aide')

    class Meta:
        verbose_name = "Dean Archbishop's Office"
        verbose_name_plural = "Dean Archbishop's Offices"

# Continue with the rest of the Dean offices...
# 6-25. Remaining Dean Offices
class DeanBishopsOffice(BaseAdministrationOffice):
    """Dean Bishops Office"""
    name = models.CharField(max_length=200, default="Dean Bishops Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_bishops_organizing_secretary')

    class Meta:
        verbose_name = "Dean Bishops Office"
        verbose_name_plural = "Dean Bishops Offices"

class DeanPastorsOffice(BaseAdministrationOffice):
    """Dean Pastors Office"""
    name = models.CharField(max_length=200, default="Dean Pastors Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_pastors_organizing_secretary')

    class Meta:
        verbose_name = "Dean Pastors Office"
        verbose_name_plural = "Dean Pastors Offices"

class DeanLayReadersOffice(BaseAdministrationOffice):
    """Dean Lay Readers Office"""
    name = models.CharField(max_length=200, default="Dean Lay Readers Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_lay_readers_organizing_secretary')

    class Meta:
        verbose_name = "Dean Lay Readers Office"
        verbose_name_plural = "Dean Lay Readers Offices"

class DeanDivisionsOffice(BaseAdministrationOffice):
    """Dean Divisions Office"""
    name = models.CharField(max_length=200, default="Dean Divisions Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_divisions_organizing_secretary')

    class Meta:
        verbose_name = "Dean Divisions Office"
        verbose_name_plural = "Dean Divisions Offices"

class DeanTeachersOffice(BaseAdministrationOffice):
    """Dean Teachers Office"""
    name = models.CharField(max_length=200, default="Dean Teachers Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_teachers_organizing_secretary')

    class Meta:
        verbose_name = "Dean Teachers Office"
        verbose_name_plural = "Dean Teachers Offices"

class DeanWomenLeadersOffice(BaseAdministrationOffice):
    """Dean Women Leaders Office"""
    name = models.CharField(max_length=200, default="Dean Women Leaders Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_women_leaders_organizing_secretary')

    class Meta:
        verbose_name = "Dean Women Leaders Office"
        verbose_name_plural = "Dean Women Leaders Offices"

class DeanEldersOffice(BaseAdministrationOffice):
    """Dean Elders Office"""
    name = models.CharField(max_length=200, default="Dean Elders Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_elders_organizing_secretary')

    class Meta:
        verbose_name = "Dean Elders Office"
        verbose_name_plural = "Dean Elders Offices"

class DeanSosoOffice(BaseAdministrationOffice):
    """Dean Soso Office - Mama/Mother, mostly wives to clerics/clergy"""
    name = models.CharField(max_length=200, default="Dean Soso Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_assistant_head')
    chairman = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_chairman')
    assistant_chair = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_assistant_chair')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_treasurer')
    organizing_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_soso_organizing_secretary')

    class Meta:
        verbose_name = "Dean Soso Office"
        verbose_name_plural = "Dean Soso Offices"

class DeanCoursesOffice(BaseAdministrationOffice):
    """Dean Courses Office"""
    name = models.CharField(max_length=200, default="Dean Courses Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_assistant_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_assistant_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_treasurer')
    assistant_treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_assistant_treasurer')
    communication_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_communication_officer')
    male_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_male_officer')
    female_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_courses_female_officer')

    class Meta:
        verbose_name = "Dean Courses Office"
        verbose_name_plural = "Dean Courses Offices"

class DeanEcclesiasticalVestmentOffice(BaseAdministrationOffice):
    """Dean Ecclesiastical/Liturgical Vestment Office"""
    name = models.CharField(max_length=200, default="Dean Ecclesiastical Vestment Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_vestment_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_vestment_assistant_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_vestment_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_vestment_treasurer')
    embroiderer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_vestment_embroiderer')
    male_tailors = models.ManyToManyField(Member, blank=True, related_name='dean_ecclesiastical_vestment_male_tailors')  # 5 tailors
    female_tailors = models.ManyToManyField(Member, blank=True, related_name='dean_ecclesiastical_vestment_female_tailors')  # 5 tailors

    class Meta:
        verbose_name = "Dean Ecclesiastical Vestment Office"
        verbose_name_plural = "Dean Ecclesiastical Vestment Offices"

class DeanEcclesiasticalCrossOffice(BaseAdministrationOffice):
    """Dean Ecclesiastical/Liturgical Cross(♱) Office"""
    name = models.CharField(max_length=200, default="Dean Ecclesiastical Cross Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_cross_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_cross_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_cross_treasurer')
    main_woodworker = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_ecclesiastical_cross_main_woodworker')
    woodworkers = models.ManyToManyField(Member, blank=True, related_name='dean_ecclesiastical_cross_woodworkers')  # up to 5

    class Meta:
        verbose_name = "Dean Ecclesiastical Cross Office"
        verbose_name_plural = "Dean Ecclesiastical Cross Offices"

class DeanChaplaincyOffice(BaseAdministrationOffice):
    """Dean Chaplaincy/Evangelism Office"""
    name = models.CharField(max_length=200, default="Dean Chaplaincy Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_chaplaincy_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_chaplaincy_assistant_head')
    officers = models.ManyToManyField(Member, blank=True, related_name='dean_chaplaincy_officers')  # 12 officers

    class Meta:
        verbose_name = "Dean Chaplaincy Office"
        verbose_name_plural = "Dean Chaplaincy Offices"

class DeanChurchesDataRecordsOffice(BaseAdministrationOffice):
    """Dean Churches Data and Records Office"""
    name = models.CharField(max_length=200, default="Dean Churches Data and Records Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_churches_data_records_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_churches_data_records_secretary')
    officers = models.ManyToManyField(Member, blank=True, related_name='dean_churches_data_records_officers')  # 8 officers

    class Meta:
        verbose_name = "Dean Churches Data and Records Office"
        verbose_name_plural = "Dean Churches Data and Records Offices"

class DeanEducationGenderEqualityOffice(BaseAdministrationOffice):
    """Dean Education and Gender Equality Office"""
    name = models.CharField(max_length=200, default="Dean Education and Gender Equality Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_education_gender_equality_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_education_gender_equality_assistant_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_education_gender_equality_secretary')
    officers = models.ManyToManyField(Member, blank=True, related_name='dean_education_gender_equality_officers')  # 4 officers

    class Meta:
        verbose_name = "Dean Education and Gender Equality Office"
        verbose_name_plural = "Dean Education and Gender Equality Offices"

class DeanDevelopmentOffice(BaseAdministrationOffice):
    """Dean Development Office"""
    name = models.CharField(max_length=200, default="Dean Development Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_development_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_development_assistant_head')
    officers = models.ManyToManyField(Member, blank=True, related_name='dean_development_officers')  # 4 officers

    class Meta:
        verbose_name = "Dean Development Office"
        verbose_name_plural = "Dean Development Offices"

class DeanDisciplinaryCommitteeOffice(BaseAdministrationOffice):
    """Dean Disciplinary Committee Office"""
    name = models.CharField(max_length=200, default="Dean Disciplinary Committee Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_disciplinary_committee_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_disciplinary_committee_assistant_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_disciplinary_committee_secretary')
    assistant_secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_disciplinary_committee_assistant_secretary')
    messenger = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_disciplinary_committee_messenger')

    class Meta:
        verbose_name = "Dean Disciplinary Committee Office"
        verbose_name_plural = "Dean Disciplinary Committee Offices"

class DeanArbitrationCommitteeOffice(BaseAdministrationOffice):
    """Dean Appeal/Justice/Arbitration Committee Office"""
    name = models.CharField(max_length=200, default="Dean Arbitration Committee Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_arbitration_committee_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_arbitration_committee_assistant_head')
    chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_arbitration_committee_chairperson')
    assistant_chairperson = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_arbitration_committee_assistant_chairperson')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_arbitration_committee_secretary')
    women_leader = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_arbitration_committee_women_leader')
    messenger = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_arbitration_committee_messenger')

    class Meta:
        verbose_name = "Dean Arbitration Committee Office"
        verbose_name_plural = "Dean Arbitration Committee Offices"

class DeanHealthCounsellingOffice(BaseAdministrationOffice):
    """Dean Health And Counselling Office"""
    name = models.CharField(max_length=200, default="Dean Health and Counselling Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_health_counselling_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_health_counselling_assistant_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_health_counselling_secretary')
    male_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_health_counselling_male_officer')
    female_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_health_counselling_female_officer')

    class Meta:
        verbose_name = "Dean Health and Counselling Office"
        verbose_name_plural = "Dean Health and Counselling Offices"

class DeanChurchesProtocolOffice(BaseAdministrationOffice):
    """Dean Churches Protocol Office"""
    name = models.CharField(max_length=200, default="Dean Churches Protocol Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_churches_protocol_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_churches_protocol_assistant_head')
    secretary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_churches_protocol_secretary')
    male_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_churches_protocol_male_officer')
    female_officer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_churches_protocol_female_officer')

    class Meta:
        verbose_name = "Dean Churches Protocol Office"
        verbose_name_plural = "Dean Churches Protocol Offices"

class DeanMediaPublicityOffice(BaseAdministrationOffice):
    """Dean Media And Publicity Office"""
    name = models.CharField(max_length=200, default="Dean Media and Publicity Office")
    
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_media_publicity_head')
    assistant_head = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_media_publicity_assistant_head')
    designer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_media_publicity_designer')

    class Meta:
        verbose_name = "Dean Media and Publicity Office"
        verbose_name_plural = "Dean Media and Publicity Offices"