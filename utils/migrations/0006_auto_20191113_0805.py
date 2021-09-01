# Generated by Django 2.1.3 on 2019-11-13 08:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_auto_20190911_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadOSMMapsRunHistory',
            fields=[
                ('download_map_run_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.TextField(default='INITIALIZED')),
                ('coordinates', models.TextField()),
                ('error', models.TextField()),
                ('last_modified_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('completed_on', models.DateTimeField(blank=True, null=True)),
                ('remove_outside_node_status', models.BooleanField(default=False)),
                ('remove_outside_node_error', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hcms_tt_download_osm_history',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TravelTimeRelatedProcesses',
            fields=[
                ('process_id', models.AutoField(primary_key=True, serialize=False)),
                ('process_name', models.TextField(blank=True, null=True)),
                ('process_no', models.IntegerField(blank=True, null=True)),
                ('process_description', models.TextField(blank=True, null=True)),
                ('process_action', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
            ],
            options={
                'db_table': 'hcms_tt_processes',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='traveltimeenginerun',
            name='error',
            field=models.TextField(blank=True, null=True),
        ),
    ]