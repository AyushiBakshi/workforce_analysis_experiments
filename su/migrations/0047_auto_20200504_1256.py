# Generated by Django 2.1.3 on 2020-05-04 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0046_auto_20200407_0534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceuser',
            name='alias',
        ),
        migrations.RemoveField(
            model_name='serviceuser',
            name='nhs_no',
        ),
        migrations.RemoveField(
            model_name='serviceuser',
            name='social_service_ref',
        ),
        migrations.RemoveField(
            model_name='serviceuser',
            name='zone_mc_id',
        ),
    ]
