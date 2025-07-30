
from django.db import models

class Equipment(models.Model):
    EQUIPMENT_STATUS = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('damaged', 'Damaged'),
        ('retired', 'Retired'),
    ]
    
    EQUIPMENT_CATEGORIES = [
        ('audio', 'Audio Equipment'),
        ('video', 'Video Equipment'),
        ('lighting', 'Lighting'),
        ('furniture', 'Furniture'),
        ('instruments', 'Musical Instruments'),
        ('computers', 'Computers & IT'),
        ('vehicles', 'Vehicles'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=EQUIPMENT_CATEGORIES)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vendor = models.CharField(max_length=200, blank=True)
    warranty_expiry = models.DateField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=EQUIPMENT_STATUS, default='available')
    location = models.CharField(max_length=200, blank=True)
    assigned_to = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    # Maintenance
    last_maintenance = models.DateField(blank=True, null=True)
    next_maintenance = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
