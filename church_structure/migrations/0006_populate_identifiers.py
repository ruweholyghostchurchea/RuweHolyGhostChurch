
# Generated manually to populate identifiers

from django.db import migrations
import random
import string


def generate_identifier(prefix):
    """Generate a unique identifier with the given prefix"""
    segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"RUWE-{prefix}-{segment1}-{segment2}"


def populate_identifiers(apps, schema_editor):
    """Populate identifiers for existing records"""
    Diocese = apps.get_model('church_structure', 'Diocese')
    Pastorate = apps.get_model('church_structure', 'Pastorate')
    Church = apps.get_model('church_structure', 'Church')
    
    # Track used identifiers to ensure uniqueness
    used_diocese_identifiers = set()
    used_pastorate_identifiers = set()
    used_church_identifiers = set()
    
    # Populate Diocese identifiers
    for diocese in Diocese.objects.filter(identifier=''):
        if diocese.name.lower() == "dean":
            diocese.identifier = "RUWE-DEAN-ROHO-0001"
        else:
            while True:
                identifier = generate_identifier('DIOS')
                if identifier not in used_diocese_identifiers:
                    used_diocese_identifiers.add(identifier)
                    diocese.identifier = identifier
                    break
        diocese.save()
    
    # Populate Pastorate identifiers
    for pastorate in Pastorate.objects.filter(identifier=''):
        while True:
            identifier = generate_identifier('PSRT')
            if identifier not in used_pastorate_identifiers:
                used_pastorate_identifiers.add(identifier)
                pastorate.identifier = identifier
                break
        pastorate.save()
    
    # Populate Church identifiers
    for church in Church.objects.filter(identifier=''):
        while True:
            identifier = generate_identifier('CRCH')
            if identifier not in used_church_identifiers:
                used_church_identifiers.add(identifier)
                church.identifier = identifier
                break
        church.save()


def reverse_populate_identifiers(apps, schema_editor):
    """Remove identifiers (for rollback)"""
    Diocese = apps.get_model('church_structure', 'Diocese')
    Pastorate = apps.get_model('church_structure', 'Pastorate')
    Church = apps.get_model('church_structure', 'Church')
    
    Diocese.objects.update(identifier='')
    Pastorate.objects.update(identifier='')
    Church.objects.update(identifier='')


class Migration(migrations.Migration):

    dependencies = [
        ('church_structure', '0005_church_identifier_diocese_identifier_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_identifiers, reverse_populate_identifiers),
    ]
