# Generated by Django 2.1.3 on 2020-04-03 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('booking', '0028_enginerun_is_stale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingchangerequest',
            name='reason',
        ),
        migrations.AddField(
            model_name='bookingchangerequest',
            name='reason_object_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bcr_reason', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='bookingchangerequest',
            name='reason_object_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
