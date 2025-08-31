
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_member_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_roles',
            field=models.JSONField(default=list, help_text='List of member roles'),
        ),
        migrations.AddField(
            model_name='member',
            name='church_clergy_roles',
            field=models.JSONField(blank=True, default=list, help_text='Church/Dean clergy roles (only if clergy role is selected)'),
        ),
        migrations.AddField(
            model_name='member',
            name='special_clergy_roles',
            field=models.JSONField(blank=True, default=list, help_text='Special clergy roles (only if clergy role is selected)'),
        ),
    ]
