# Generated by Django 2.1.3 on 2020-06-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0040_auto_20200617_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledbooking',
            name='is_unresolved',
            field=models.BooleanField(default=False),
        ),
    ]