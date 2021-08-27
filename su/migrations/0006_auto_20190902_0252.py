# Generated by Django 2.1.3 on 2019-09-02 02:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0005_mar_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suweeklybooking',
            name='medications',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='suweeklybooking',
            name='tasks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
