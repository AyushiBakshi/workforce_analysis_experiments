# Generated by Django 2.1.3 on 2020-02-26 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0026_auto_20200115_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledbooking',
            name='is_notified',
            field=models.BooleanField(default=False),
        ),
    ]