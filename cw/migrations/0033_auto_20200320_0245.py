# Generated by Django 2.1.3 on 2020-03-20 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

def add_mc(apps, schema_editor):
    HcmsUtilsMasterCode = apps.get_model('utils', 'HcmsUtilsMasterCode')
    from django.utils import timezone

    HcmsUtilsMasterCode.objects.create(
        code_type = "TERMINATION_REQUEST_STATUS",
        code_no = 1,
        code_val = "Approved",
        created_date = timezone.now(),
        created_by = 1,
        last_modified_date = timezone.now(),
        last_modified_by = 1,
        delete_ind = 'N'
    )
    HcmsUtilsMasterCode.objects.create(
        code_type = "TERMINATION_REQUEST_STATUS",
        code_no = 2,
        code_val = "Pending",
        created_date = timezone.now(),
        created_by = 1,
        last_modified_date = timezone.now(),
        last_modified_by = 1,
        delete_ind = 'N'
    )
    HcmsUtilsMasterCode.objects.create(
        code_type = "TERMINATION_REQUEST_STATUS",
        code_no = 3,
        code_val = "Rejected",
        created_date = timezone.now(),
        created_by = 1,
        last_modified_date = timezone.now(),
        last_modified_by = 1,
        delete_ind = 'N'
    )
    HcmsUtilsMasterCode.objects.create(
        code_type = "TERMINATION_REQUEST_STATUS",
        code_no = 4,
        code_val = "HR Approved",
        created_date = timezone.now(),
        created_by = 1,
        last_modified_date = timezone.now(),
        last_modified_by = 1,
        delete_ind = 'N'
    )

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cw', '0032_auto_20200318_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerminationRequest',
            fields=[
                ('termination_request_id', models.AutoField(primary_key=True, serialize=False)),
                ('proposed_date', models.DateTimeField()),
                ('remark', models.TextField(blank=True, null=True)),
                ('termination_request_status_mc_id', models.IntegerField(blank=True, null=True)),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_date', models.DateTimeField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='terminate_approver', to=settings.AUTH_USER_MODEL)),
                ('request_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminate_requester', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminate_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_cw_termination_request',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='employmentrecord',
            name='termination_request',
        ),
        migrations.RunPython(add_mc),
    ]
