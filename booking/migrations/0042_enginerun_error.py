# Generated by Django 2.1.3 on 2020-06-19 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0041_scheduledbooking_is_unresolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='enginerun',
            name='error',
            field=models.TextField(blank=True, null=True),
        ),
    ]
