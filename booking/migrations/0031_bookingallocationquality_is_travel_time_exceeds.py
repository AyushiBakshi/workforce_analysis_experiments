# Generated by Django 2.1.3 on 2020-04-09 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0030_auto_20200409_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingallocationquality',
            name='is_travel_time_exceeds',
            field=models.BooleanField(default=False),
        ),
    ]