# Generated by Django 2.1.3 on 2021-04-03 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0058_auto_20210323_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingslot',
            name='training_slot_status_mc_id',
            field=models.IntegerField(blank=True, default=1184, null=True),
        ),
    ]
