# Generated by Django 2.1.3 on 2020-01-23 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0022_remove_careworker_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employmentrecord',
            name='availability_hr',
            field=models.IntegerField(default=32),
            preserve_default=False,
        ),
    ]
