# Generated by Django 2.1.3 on 2021-01-20 06:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0064_suweeklybooking_freq_ref_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suweeklybooking',
            name='fixed_cws',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, size=None),
        ),
    ]
