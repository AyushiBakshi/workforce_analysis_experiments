# Generated by Django 2.1.3 on 2019-10-18 06:14

from django.db import migrations, models

def insert_master_code(apps, schema_editor):
    HcmsUtilsMasterCode = apps.get_model('utils', 'HcmsUtilsMasterCode')
    from django.utils import timezone
    HcmsUtilsMasterCode.objects.create(
        code_id = 1096,
        code_type = "PAY_FREQUENCY",
        code_no = 1,
        code_val = "Monthly",
        created_date = timezone.now(),
        created_by = 1,
        last_modified_date = timezone.now(),
        last_modified_by = 1,
        delete_ind = 'N'
    )
    HcmsUtilsMasterCode.objects.create(
        code_id = 1097,
        code_type = "PAY_FREQUENCY",
        code_no = 2,
        code_val = "Weekly",
        created_date = timezone.now(),
        created_by = 1,
        last_modified_date = timezone.now(),
        last_modified_by = 1,
        delete_ind = 'N'
    )

def migrate_data(apps, schema_editor):
    EmploymentRecord = apps.get_model('cw', 'EmploymentRecord')
    import random

    rates = [20,30,25]
    frequencies = [20,30,25]

    for e in EmploymentRecord.objects.all():
        e.pay_rate = rates[random.randrange(0,3)]
        e.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0007_auto_20190911_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='employmentrecord',
            name='pay_frequency_mc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employmentrecord',
            name='pay_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.RunPython(insert_master_code),
        migrations.RunPython(migrate_data),
    ]
