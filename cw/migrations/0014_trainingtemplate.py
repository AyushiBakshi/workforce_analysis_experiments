# Generated by Django 2.1.3 on 2019-12-06 06:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0013_auto_20191205_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingTemplate',
            fields=[
                ('training_template_id', models.AutoField(primary_key=True, serialize=False)),
                ('training_type', models.CharField(blank=True, max_length=200, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('validity', models.IntegerField(blank=True, null=True)),
                ('items_covered', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=None)),
                ('init_training', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'hcms_cw_training_template',
                'managed': True,
            },
        ),
    ]
