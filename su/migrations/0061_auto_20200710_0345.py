# Generated by Django 2.1.3 on 2020-07-10 03:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('su', '0060_auto_20200707_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='CWException',
            fields=[
                ('cw_exception_id', models.AutoField(primary_key=True, serialize=False)),
                ('exceptions', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cw_exceptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_su_cw_exception',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='serviceuser',
            name='exceptions',
        ),
    ]
