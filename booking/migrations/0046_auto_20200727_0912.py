# Generated by Django 2.1.3 on 2020-07-27 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0045_auto_20200727_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingallocation',
            name='booking_quality',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
