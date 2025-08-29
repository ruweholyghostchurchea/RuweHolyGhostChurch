
# Generated manually to update leadership fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_member_identifier'),
        ('church_structure', '0006_populate_identifiers'),
    ]

    operations = [
        # Add new ForeignKey fields
        migrations.AddField(
            model_name='diocese',
            name='bishop',
            field=models.ForeignKey(blank=True, help_text='Search and select a member as bishop', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dioceses_as_bishop', to='members.member'),
        ),
        migrations.AddField(
            model_name='pastorate',
            name='pastor',
            field=models.ForeignKey(blank=True, help_text='Search and select a member as pastor', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pastorates_as_pastor', to='members.member'),
        ),
        migrations.AddField(
            model_name='church',
            name='head_teacher',
            field=models.ForeignKey(blank=True, help_text='Search and select a member as head teacher', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='churches_as_head_teacher', to='members.member'),
        ),
        migrations.AddField(
            model_name='church',
            name='teachers',
            field=models.ManyToManyField(blank=True, help_text='Search and select up to 12 additional teachers', related_name='churches_as_teacher', to='members.member'),
        ),
        # Remove old CharField fields
        migrations.RemoveField(
            model_name='diocese',
            name='bishop_name',
        ),
        migrations.RemoveField(
            model_name='diocese',
            name='bishop_phone',
        ),
        migrations.RemoveField(
            model_name='diocese',
            name='bishop_email',
        ),
        migrations.RemoveField(
            model_name='pastorate',
            name='pastor_name',
        ),
        migrations.RemoveField(
            model_name='pastorate',
            name='pastor_phone',
        ),
        migrations.RemoveField(
            model_name='pastorate',
            name='pastor_email',
        ),
        migrations.RemoveField(
            model_name='church',
            name='head_teacher_name',
        ),
        migrations.RemoveField(
            model_name='church',
            name='head_teacher_phone',
        ),
        migrations.RemoveField(
            model_name='church',
            name='head_teacher_email',
        ),
        migrations.RemoveField(
            model_name='church',
            name='assistant_teachers',
        ),
    ]
