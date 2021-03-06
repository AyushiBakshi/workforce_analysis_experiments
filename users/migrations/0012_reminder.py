# Generated by Django 2.1.3 on 2020-01-16 03:35

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200110_0539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('reminder_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('respond_by', models.DateTimeField(blank=True, null=True)),
                ('attachments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminder_receiver', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reminder_actor', to=settings.AUTH_USER_MODEL)),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reminder_caller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_reminder',
                'managed': True,
            },
        ),
    ]
