# Generated by Django 2.1.3 on 2019-11-11 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0017_suweeklybooking_change_requests'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='schedulecr',
            table='hcms_su_schedule_cr',
        ),
    ]
