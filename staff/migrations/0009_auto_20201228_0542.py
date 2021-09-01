# Generated by Django 2.1.3 on 2020-12-28 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_staffbankdetail_branch_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffleavesummary',
            name='annual_leave_accrued',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='staffleavesummary',
            name='days_per_week',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
        migrations.AddField(
            model_name='staffleavesummary',
            name='medical_leave_accrued',
            field=models.FloatField(default=0),
        ),
    ]