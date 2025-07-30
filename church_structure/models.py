
from django.db import models

class Diocese(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, choices=[
        ('Kenya', 'Kenya'),
        ('Uganda', 'Uganda'),
        ('Tanzania', 'Tanzania')
    ])
    bishop_name = models.CharField(max_length=200)
    bishop_phone = models.CharField(max_length=20, blank=True)
    bishop_email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['country', 'name']
        verbose_name = 'Diocese'
        verbose_name_plural = 'Dioceses'
    
    def __str__(self):
        return f"{self.name} - {self.country}"

class Pastorate(models.Model):
    name = models.CharField(max_length=200)
    diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, related_name='pastorates')
    pastor_name = models.CharField(max_length=200)
    pastor_phone = models.CharField(max_length=20, blank=True)
    pastor_email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['diocese', 'name']
        verbose_name = 'Pastorate'
        verbose_name_plural = 'Pastorates'
    
    def __str__(self):
        return f"{self.name} - {self.diocese.name}"

class Church(models.Model):
    name = models.CharField(max_length=200)
    pastorate = models.ForeignKey(Pastorate, on_delete=models.CASCADE, related_name='churches')
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    head_teacher_name = models.CharField(max_length=200)
    head_teacher_phone = models.CharField(max_length=20, blank=True)
    head_teacher_email = models.EmailField(blank=True)
    assistant_teachers = models.TextField(blank=True, help_text="List additional church teachers, one per line")
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
    
    def __str__(self):
        return f"{self.name} - {self.pastorate.name}"
    
    @property
    def diocese(self):
        return self.pastorate.diocese
    
    @property
    def full_hierarchy(self):
        return f"{self.diocese.name} > {self.pastorate.name} > {self.name}"
