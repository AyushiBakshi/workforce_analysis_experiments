# Generated by Django 2.1.3 on 2019-10-25 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20191018_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledbooking',
            name='funding_type_mc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
