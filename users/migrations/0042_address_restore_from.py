# Generated by Django 2.1.3 on 2021-05-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_address_is_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='restore_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]