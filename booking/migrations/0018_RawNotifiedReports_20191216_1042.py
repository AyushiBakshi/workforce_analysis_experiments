# Generated by Django 2.1.3 on 2019-12-16 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0017_auto_20191214_0700'),
        ('booking', '0017_merge_20191214_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enginerun',
            name='engine_run_raw_report',
        ),
        migrations.AddField(
            model_name='enginerun',
            name='notified_report',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notified_doc', to='cw.Document'),
        ),
        migrations.AddField(
            model_name='enginerun',
            name='raw_report',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='raw_doc', to='cw.Document'),
        ),
    ]
