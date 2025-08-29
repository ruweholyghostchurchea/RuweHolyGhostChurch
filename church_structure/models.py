
from django.db import models
from django.utils.text import slugify
import random
import string

class Diocese(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=20, unique=True, blank=True, help_text="Auto-generated unique identifier")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    country = models.CharField(max_length=100, choices=[
        ('Kenya', 'Kenya'),
        ('Uganda', 'Uganda'),
        ('Tanzania', 'Tanzania')
    ])
    bishop = models.ForeignKey('members.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='dioceses_as_bishop', help_text="Search and select a member as bishop")
    description = models.TextField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['country', 'name']
        verbose_name = 'Diocese'
        verbose_name_plural = 'Dioceses'
    
    def generate_identifier(self):
        """Generate a unique identifier for the diocese"""
        if self.name.lower() == "dean":
            return "RUWE-DEAN-ROHO-0001"
        
        while True:
            # Generate random 4-character segments
            segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            identifier = f"RUWE-DIOS-{segment1}-{segment2}"
            
            # Check if this identifier already exists
            if not Diocese.objects.filter(identifier=identifier).exists():
                return identifier

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_identifier()
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.country}")
        super().save(*args, **kwargs)
    
    @property
    def bishop_name(self):
        return self.bishop.full_name if self.bishop else "Not assigned"
    
    @property
    def bishop_phone(self):
        return self.bishop.phone_number if self.bishop else ""
    
    @property
    def bishop_email(self):
        return self.bishop.email_address if self.bishop else ""

    def __str__(self):
        return f"{self.name} - {self.country}"

class Pastorate(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=20, unique=True, blank=True, help_text="Auto-generated unique identifier")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, related_name='pastorates')
    pastor = models.ForeignKey('members.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='pastorates_as_pastor', help_text="Search and select a member as pastor")
    description = models.TextField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['diocese', 'name']
        verbose_name = 'Pastorate'
        verbose_name_plural = 'Pastorates'
    
    def generate_identifier(self):
        """Generate a unique identifier for the pastorate"""
        while True:
            # Generate random 4-character segments
            segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            identifier = f"RUWE-PSRT-{segment1}-{segment2}"
            
            # Check if this identifier already exists
            if not Pastorate.objects.filter(identifier=identifier).exists():
                return identifier

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_identifier()
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.diocese.name}")
        super().save(*args, **kwargs)
    
    @property
    def pastor_name(self):
        return self.pastor.full_name if self.pastor else "Not assigned"
    
    @property
    def pastor_phone(self):
        return self.pastor.phone_number if self.pastor else ""
    
    @property
    def pastor_email(self):
        return self.pastor.email_address if self.pastor else ""
    
    def __str__(self):
        return f"{self.name} - {self.diocese.name}"

class Church(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=20, unique=True, blank=True, help_text="Auto-generated unique identifier")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    pastorate = models.ForeignKey(Pastorate, on_delete=models.CASCADE, related_name='churches')
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    head_teacher = models.ForeignKey('members.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='churches_as_head_teacher', help_text="Search and select a member as head teacher")
    teachers = models.ManyToManyField('members.Member', blank=True, related_name='churches_as_teacher', help_text="Search and select up to 12 additional teachers")
    service_times = models.TextField(blank=True, help_text="Service schedule information")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['pastorate', 'name']
        verbose_name = 'Church'
        verbose_name_plural = 'Churches'
    
    def generate_identifier(self):
        """Generate a unique identifier for the church"""
        while True:
            # Generate random 4-character segments
            segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            identifier = f"RUWE-CRCH-{segment1}-{segment2}"
            
            # Check if this identifier already exists
            if not Church.objects.filter(identifier=identifier).exists():
                return identifier

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_identifier()
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.pastorate.name}")
        super().save(*args, **kwargs)
    
    @property
    def head_teacher_name(self):
        return self.head_teacher.full_name if self.head_teacher else "Not assigned"
    
    @property
    def head_teacher_phone(self):
        return self.head_teacher.phone_number if self.head_teacher else ""
    
    @property
    def head_teacher_email(self):
        return self.head_teacher.email_address if self.head_teacher else ""
    
    @property
    def assistant_teachers(self):
        teachers_list = list(self.teachers.all())
        if teachers_list:
            return "\n".join([teacher.full_name for teacher in teachers_list])
        return "No additional teachers assigned"
    
    @property
    def teachers_count(self):
        return self.teachers.count()
    
    def can_add_teacher(self):
        return self.teachers.count() < 12
    
    def __str__(self):
        return f"{self.name} - {self.pastorate.name}"
    
    @property
    def diocese(self):
        return self.pastorate.diocese
    
    @property
    def full_hierarchy(self):
        return f"{self.diocese.name} > {self.pastorate.name} > {self.name}"
