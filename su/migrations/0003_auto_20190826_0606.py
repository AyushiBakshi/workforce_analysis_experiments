# Generated by Django 2.1.3 on 2019-08-26 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0002_auto_20190823_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='need_help_cooking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='observation',
            name='need_help_with_laundry',
            field=models.BooleanField(default=False),
        ),
    ]
