# Generated by Django 2.1.3 on 2020-06-22 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0044_cwavailability_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='note',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]