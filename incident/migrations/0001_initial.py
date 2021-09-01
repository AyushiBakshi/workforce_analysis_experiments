# Generated by Django 2.1.3 on 2019-08-14 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('incident_id', models.AutoField(primary_key=True, serialize=False)),
                ('reported_by_user', models.IntegerField(blank=True, null=True)),
                ('reported_by_unregistered_user', models.CharField(blank=True, max_length=150, null=True)),
                ('reported_date', models.DateTimeField(blank=True, null=True)),
                ('incident_date', models.DateTimeField(blank=True, null=True)),
                ('incident_location', models.CharField(blank=True, max_length=200, null=True)),
                ('incident_details', models.TextField(blank=True, null=True)),
                ('witness_user', models.IntegerField(blank=True, null=True)),
                ('witness_details', models.TextField(blank=True, null=True)),
                ('is_treatment_provided', models.BooleanField(default=False)),
                ('is_injury_occurred', models.BooleanField(default=False)),
                ('injury_description', models.TextField(blank=True, null=True)),
                ('related_booking_id', models.IntegerField(blank=True, null=True)),
                ('incident_status_mc_id', models.IntegerField(blank=True, null=True)),
                ('admin_remark', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('about_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incident', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_incident',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='IncidentReport',
            fields=[
                ('incident_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_urgent', models.BooleanField(default=False)),
                ('reporter_role_id', models.SmallIntegerField(blank=True, null=True)),
                ('reporter_staff', models.IntegerField(blank=True, null=True)),
                ('reporter_non_staff', models.CharField(blank=True, max_length=150, null=True)),
                ('reporter_phone', models.CharField(blank=True, max_length=45, null=True)),
                ('for_user', models.IntegerField(blank=True, null=True)),
                ('reporter_note', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('admin_remark', models.TextField(blank=True, null=True)),
                ('action_items_done', models.CharField(blank=True, max_length=200, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incident_report', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_incident_report',
                'managed': True,
            },
        ),
    ]