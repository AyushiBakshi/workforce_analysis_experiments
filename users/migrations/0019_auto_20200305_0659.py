# Generated by Django 2.1.3 on 2020-03-05 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_log_record_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='is_mailing_address',
        ),
        migrations.AddField(
            model_name='address',
            name='is_current_address',
            field=models.BooleanField(default=True),
        ),
    ]
