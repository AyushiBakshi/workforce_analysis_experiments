# Generated by Django 2.1.3 on 2019-10-17 09:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0008_auto_20191017_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='mobility_equipment_mc_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), default=list, size=None),
        ),
    ]
