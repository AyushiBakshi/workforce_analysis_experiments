# Generated by Django 2.1.3 on 2019-09-09 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_address_is_add_outside_business_boundary'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='misc_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]