# Generated by Django 2.1.3 on 2020-06-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0038_auto_20200611_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingallocation',
            name='is_changed',
            field=models.BooleanField(default=False),
        ),
    ]
