# Generated by Django 2.1.3 on 2019-12-18 04:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0036_auto_20191205_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suweeklybooking',
            name='consumables',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
