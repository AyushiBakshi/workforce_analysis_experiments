# Generated by Django 2.1.3 on 2019-08-31 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0003_auto_20190826_0606'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingchangerequest',
            name='schedule_override',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='so_id', to='su.SuScheduleOverrides'),
        ),
    ]
