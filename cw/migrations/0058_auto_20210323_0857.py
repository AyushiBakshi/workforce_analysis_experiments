# Generated by Django 2.1.3 on 2021-03-23 08:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0057_leavesummary_medical_leave_accrued'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingSlot',
            fields=[
                ('training_slot_id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('arrival_time', models.TimeField(blank=True, null=True)),
                ('training_slot_status_mc_id', models.IntegerField(blank=True, default=1183, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
            ],
            options={
                'db_table': 'hcms_cw_training_slots',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='training',
            name='approved_by_fin',
        ),
        migrations.RemoveField(
            model_name='training',
            name='approved_by_hr',
        ),
        migrations.RemoveField(
            model_name='training',
            name='arrival_time',
        ),
        migrations.RemoveField(
            model_name='training',
            name='award_expires_on',
        ),
        migrations.RemoveField(
            model_name='training',
            name='completed_on',
        ),
        migrations.RemoveField(
            model_name='training',
            name='receipt_doc_id',
        ),
        migrations.RemoveField(
            model_name='training',
            name='report_doc_id',
        ),
        migrations.RemoveField(
            model_name='training',
            name='training_start_date',
        ),
        migrations.AddField(
            model_name='trainingslot',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cw_training', to='cw.Training'),
        ),
    ]
