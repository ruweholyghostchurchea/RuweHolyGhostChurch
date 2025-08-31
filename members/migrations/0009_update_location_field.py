
# Generated migration for updating location field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_update_job_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='location',
            field=models.CharField(help_text='Location (city, country)', max_length=200),
        ),
    ]
