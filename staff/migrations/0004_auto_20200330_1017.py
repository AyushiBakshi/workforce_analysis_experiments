# Generated by Django 2.1.3 on 2020-03-30 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0003_staffbankdetail_staffrecruitment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('visa_status_mc_id', models.IntegerField(blank=True, null=True)),
                ('visa_expiry_date', models.DateTimeField(blank=True, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=200, null=True)),
                ('passport_expiry_date', models.DateTimeField(blank=True, null=True)),
                ('access_card_number', models.CharField(blank=True, max_length=200, null=True)),
                ('payroll_number', models.CharField(blank=True, max_length=45, null=True)),
                ('nationality_mc_id', models.IntegerField(blank=True, null=True)),
                ('staff_status_mc_id', models.IntegerField(blank=True, null=True)),
                ('passport_doc_id', models.IntegerField(blank=True, null=True)),
                ('visa_doc_id', models.IntegerField(blank=True, null=True)),
                ('residency_proof_doc_id', models.IntegerField(blank=True, null=True)),
                ('is_permanent_uk_resident', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_staff_staff',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StaffSuspendedRecord',
            fields=[
                ('suspended_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('started_date', models.DateTimeField(blank=True, null=True)),
                ('finished_date', models.DateTimeField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('suspend_status_mc_id', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_suspended_record', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_staff_suspended_record',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='staffemploymentrecord',
            name='job_title',
        ),
        migrations.AddField(
            model_name='staffbankdetail',
            name='account_type_mc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staffemploymentrecord',
            name='contract_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staffemploymentrecord',
            name='revised_origin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
