# Generated by Django 2.1.3 on 2021-06-01 07:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0064_auto_20210512_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilltemplate',
            name='is_mandatory',
            field=models.BooleanField(default=False),
        )
    ]