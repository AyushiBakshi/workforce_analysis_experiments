# Generated by Django 2.1.3 on 2020-06-04 12:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0051_auto_20200515_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observation',
            name='client_type_mc_id',
        ),
        migrations.AddField(
            model_name='observation',
            name='client_type_mc_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), default=list, size=None),
        ),
    ]
