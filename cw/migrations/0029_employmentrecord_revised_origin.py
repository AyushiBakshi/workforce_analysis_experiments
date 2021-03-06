# Generated by Django 2.1.3 on 2020-03-10 08:23

from django.db import migrations, models

def add_mc(apps, schema_editor):
    HcmsUtilsMasterCode = apps.get_model('utils', 'HcmsUtilsMasterCode')
    from django.utils import timezone

    HcmsUtilsMasterCode.objects.create(
        code_type = "EMPLOYMENT_STATUS",
        code_no = 4,
        code_val = "Revised",
        created_date = timezone.now(),
        created_by = 1,
        last_modified_date = timezone.now(),
        last_modified_by = 1,
        delete_ind = 'N'
    )
class Migration(migrations.Migration):


    dependencies = [
        ('cw', '0028_auto_20200218_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='employmentrecord',
            name='revised_origin',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(add_mc),
    ]
