# Generated by Django 2.1.3 on 2020-06-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0041_leavesummary_urgent_leave_days_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavesummary',
            name='leave_of_absence_days_taken',
            field=models.FloatField(default=0),
        ),
    ]
