# Generated by Django 2.1.3 on 2020-05-04 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_user_channel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nhs_no',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]