# Generated by Django 2.1.3 on 2019-12-04 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0005_trigger_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='closed_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='closed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
