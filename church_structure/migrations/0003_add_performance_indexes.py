
# Generated manually for performance optimization

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_structure', '0002_initial'),
        ('members', '0001_initial'),
    ]

    operations = [
        # Add indexes for Diocese
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_diocese_active ON church_structure_diocese (is_active) WHERE is_active = true;",
            reverse_sql="DROP INDEX IF EXISTS idx_diocese_active;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_diocese_country_name ON church_structure_diocese (country, name);",
            reverse_sql="DROP INDEX IF EXISTS idx_diocese_country_name;"
        ),
        
        # Add indexes for Pastorate
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pastorate_active ON church_structure_pastorate (is_active) WHERE is_active = true;",
            reverse_sql="DROP INDEX IF EXISTS idx_pastorate_active;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pastorate_diocese_name ON church_structure_pastorate (diocese_id, name);",
            reverse_sql="DROP INDEX IF EXISTS idx_pastorate_diocese_name;"
        ),
        
        # Add indexes for Church
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_church_active ON church_structure_church (is_active) WHERE is_active = true;",
            reverse_sql="DROP INDEX IF EXISTS idx_church_active;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_church_pastorate_name ON church_structure_church (pastorate_id, name);",
            reverse_sql="DROP INDEX IF EXISTS idx_church_pastorate_name;"
        ),
    ]
