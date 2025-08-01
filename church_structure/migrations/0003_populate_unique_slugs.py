
# Generated manually to populate unique slugs before adding constraints

from django.db import migrations
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    """Populate slug fields with unique values"""
    Diocese = apps.get_model('church_structure', 'Diocese')
    Pastorate = apps.get_model('church_structure', 'Pastorate')
    Church = apps.get_model('church_structure', 'Church')
    
    # Populate Diocese slugs
    used_diocese_slugs = set()
    for diocese in Diocese.objects.all():
        base_slug = slugify(f"{diocese.name}-{diocese.country}")
        slug = base_slug
        counter = 1
        while slug in used_diocese_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        diocese.slug = slug
        diocese.save()
        used_diocese_slugs.add(slug)
    
    # Populate Pastorate slugs
    used_pastorate_slugs = set()
    for pastorate in Pastorate.objects.all():
        base_slug = slugify(f"{pastorate.name}-{pastorate.diocese.name}")
        slug = base_slug
        counter = 1
        while slug in used_pastorate_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        pastorate.slug = slug
        pastorate.save()
        used_pastorate_slugs.add(slug)
    
    # Populate Church slugs
    used_church_slugs = set()
    for church in Church.objects.all():
        base_slug = slugify(f"{church.name}-{church.pastorate.name}")
        slug = base_slug
        counter = 1
        while slug in used_church_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        church.slug = slug
        church.save()
        used_church_slugs.add(slug)

def reverse_populate_slugs(apps, schema_editor):
    """Clear slug fields"""
    Diocese = apps.get_model('church_structure', 'Diocese')
    Pastorate = apps.get_model('church_structure', 'Pastorate')
    Church = apps.get_model('church_structure', 'Church')
    
    Diocese.objects.update(slug='')
    Pastorate.objects.update(slug='')
    Church.objects.update(slug='')

class Migration(migrations.Migration):

    dependencies = [
        ('church_structure', '0002_add_slug_fields_no_unique'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
    ]
