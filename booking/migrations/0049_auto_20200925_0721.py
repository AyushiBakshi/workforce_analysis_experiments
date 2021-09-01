# Generated by Django 2.1.3 on 2020-09-25 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0048_auto_20200902_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enginerun',
            name='is_cp_priority_high',
        ),
        migrations.AddField(
            model_name='enginerun',
            name='critical_booking_priority',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enginerun',
            name='private_booking_priority',
            field=models.FloatField(blank=True, null=True),
        ),
    ]