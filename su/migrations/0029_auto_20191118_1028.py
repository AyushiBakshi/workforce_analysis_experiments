# Generated by Django 2.1.3 on 2019-11-18 10:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0028_auto_20191118_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suweeklybooking',
            name='b_gen_comment',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
