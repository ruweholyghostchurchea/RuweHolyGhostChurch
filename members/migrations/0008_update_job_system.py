
# Generated migration for job system update

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_alter_member_user_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='job_occupations',
            field=models.JSONField(default=list, help_text='List of selected job/occupation roles'),
        ),
        migrations.AddField(
            model_name='member',
            name='income_details',
            field=models.TextField(blank=True, help_text='Additional income and occupation details'),
        ),
        migrations.RemoveField(
            model_name='member',
            name='job_occupation_income',
        ),
    ]
