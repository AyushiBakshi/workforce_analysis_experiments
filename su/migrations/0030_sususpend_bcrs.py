# Generated by Django 2.1.3 on 2019-11-25 03:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0029_auto_20191118_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='sususpend',
            name='bcrs',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
