# Generated by Django 2.1.3 on 2020-01-14 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0020_auto_20200110_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilityslot',
            name='biweekly',
        ),
        migrations.AddField(
            model_name='availabilityslot',
            name='biweekly_mc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
