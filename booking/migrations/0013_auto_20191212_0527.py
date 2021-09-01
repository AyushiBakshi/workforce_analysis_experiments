# Generated by Django 2.1.3 on 2019-12-12 05:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_tasktemplate_booking_type_mc_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktemplate',
            name='booking_type_mc_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(10, 'Social Activities'), (11, 'Respite Care'), (12, 'Overnight Care'), (13, 'Live-in Care'), (14, 'Sitting-in Care'), (15, 'Domestic Care'), (16, 'Personal Care')]), size=None), default=list, size=None),
        ),
    ]