# Generated by Django 2.1.3 on 2020-07-07 13:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0057_auto_20200707_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='sususpend',
            name='attachments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]
