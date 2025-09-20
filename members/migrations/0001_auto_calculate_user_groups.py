
# Generated migration for auto-calculating user groups

from django.db import migrations
from datetime import date

def calculate_user_groups(apps, schema_editor):
    Member = apps.get_model('members', 'Member')
    
    for member in Member.objects.all():
        if member.date_of_birth:
            today = date.today()
            age = today.year - member.date_of_birth.year - ((today.month, today.day) < (member.date_of_birth.month, member.date_of_birth.day))
            
            if 18 <= age <= 35:
                member.user_group = 'Youth'
            elif 36 <= age <= 60:
                member.user_group = 'Adult'
            elif age >= 61:
                member.user_group = 'Elder'
            else:
                member.user_group = 'Adult'  # Default fallback
            
            member.save()

def reverse_calculate_user_groups(apps, schema_editor):
    # This migration is not reversible as we don't store the old values
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('members', '__latest__'),  # Replace with your latest migration number
    ]

    operations = [
        migrations.RunPython(calculate_user_groups, reverse_calculate_user_groups),
    ]
