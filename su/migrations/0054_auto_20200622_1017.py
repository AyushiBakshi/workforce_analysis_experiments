# Generated by Django 2.1.3 on 2020-06-22 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0053_auto_20200610_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalhistory',
            name='note',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]