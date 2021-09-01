# Generated by Django 2.1.3 on 2021-05-19 03:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0051_medicationprescriptionconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataLock',
            fields=[
                ('data_lock_id', models.AutoField(primary_key=True, serialize=False)),
                ('object_id', models.IntegerField(blank=True, null=True)),
                ('object_type', models.CharField(blank=True, max_length=150, null=True)),
                ('locked_by_user_name', models.CharField(blank=True, max_length=50, null=True)),
                ('user_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_modified_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'hcms_utils_data_lock',
                'managed': True,
            },
        ),
    ]