# Generated by Django 2.1.3 on 2020-10-08 07:38

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_reminder_original_reminder'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdminAccess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last Modified On')),
                ('users_selected', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Users Selected'), blank=True, null=True, size=None)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('remarks', models.CharField(blank=True, max_length=200, null=True, verbose_name='Remarks')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By')),
            ],
            options={
                'db_table': 'hcms_um_user_admin_access',
                'managed': True,
            },
        ),
    ]
