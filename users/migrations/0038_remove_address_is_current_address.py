# Generated by Django 2.1.3 on 2021-03-26 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_address_bookings_handled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='is_current_address',
        ),
    ]
