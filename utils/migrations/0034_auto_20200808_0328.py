# Generated by Django 2.1.3 on 2020-08-08 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0033_auto_20200808_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traveltimerelatedprocesseshistory',
            old_name='engine_run_last_modified_date',
            new_name='engine_progress_last_modified_date',
        ),
        migrations.RemoveField(
            model_name='traveltimerelatedprocesseshistory',
            name='map_last_modified_date',
        ),
    ]
