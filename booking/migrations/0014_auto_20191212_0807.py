# Generated by Django 2.1.3 on 2019-12-12 08:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_auto_20191212_0527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktemplate',
            name='booking_type_mc_id',
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='booking_types',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), default=list, size=None),
        ),
    ]