# Generated by Django 2.1.3 on 2020-08-12 08:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0042_auto_20200811_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='traveltimecoordinatesavehistory',
            name='excluded_cw',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150, null=True), default=list, size=None),
        ),
        migrations.AddField(
            model_name='traveltimecoordinatesavehistory',
            name='excluded_su',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150, null=True), default=list, size=None),
        ),
    ]
