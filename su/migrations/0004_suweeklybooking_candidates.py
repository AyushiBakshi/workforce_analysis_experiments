# Generated by Django 2.1.3 on 2019-08-29 03:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0003_auto_20190826_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='suweeklybooking',
            name='candidates',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
