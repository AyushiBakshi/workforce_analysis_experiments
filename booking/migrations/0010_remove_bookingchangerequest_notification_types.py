# Generated by Django 2.1.3 on 2019-11-28 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20191118_0339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingchangerequest',
            name='notification_types',
        ),
    ]
