
# Generated migration for church model updates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_structure', '0008_alter_diocese_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='church',
            old_name='address',
            new_name='location',
        ),
        migrations.AddField(
            model_name='church',
            name='map_link',
            field=models.URLField(blank=True, help_text='Google Maps link for exact church location'),
        ),
        migrations.AddField(
            model_name='church',
            name='is_mission_church',
            field=models.BooleanField(default=False, verbose_name='Mission Church'),
        ),
        migrations.AddField(
            model_name='church',
            name='is_diosen_church',
            field=models.BooleanField(default=False, verbose_name='Diosen Church'),
        ),
        migrations.AddField(
            model_name='church',
            name='is_headquarter_church',
            field=models.BooleanField(default=False, verbose_name='Headquarter Church'),
        ),
        migrations.AlterField(
            model_name='church',
            name='service_times',
            field=models.CharField(choices=[('6:00 AM Saturday', '6:00 AM Saturday'), ('9:00 AM Saturday', '9:00 AM Saturday'), ('12:00 NOON Saturday', '12:00 NOON Saturday'), ('3:00 PM Saturday', '3:00 PM Saturday')], default='9:00 AM Saturday', help_text='Service time on Saturday', max_length=50),
        ),
    ]
