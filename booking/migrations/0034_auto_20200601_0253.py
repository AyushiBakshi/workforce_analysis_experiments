# Generated by Django 2.1.3 on 2020-06-01 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0033_bookingallocationquality_travel_time2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engineconfig',
            name='engine_run',
        ),
        migrations.RenameField(
            model_name='enginerun',
            old_name='min_util_rate',
            new_name='change_percentage',
        ),
        migrations.DeleteModel(
            name='EngineConfig',
        ),
    ]