# Generated by Django 2.1.3 on 2020-06-10 01:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0052_auto_20200604_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='client_type_mc_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='observation',
            name='mobility_equipment_mc_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]
