# Generated by Django 2.1.3 on 2020-04-14 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20200401_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='channel_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
