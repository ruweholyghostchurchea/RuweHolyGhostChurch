
from django.db import models
from members.models import Member

class OfferingCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Offering Categories'
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Offering(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(OfferingCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    # Anonymous donation handling
    donor_name = models.CharField(max_length=200, blank=True, help_text="For anonymous donations")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        
    def __str__(self):
        donor = self.member.full_name if self.member else (self.donor_name or "Anonymous")
        return f"{donor} - ${self.amount} ({self.category.name})"

class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('equipment', 'Equipment'),
        ('ministry', 'Ministry'),
        ('outreach', 'Outreach'),
        ('administrative', 'Administrative'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    vendor = models.CharField(max_length=200, blank=True)
    receipt_number = models.CharField(max_length=100, blank=True)
    approved_by = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        
    def __str__(self):
        return f"{self.description} - ${self.amount}"
