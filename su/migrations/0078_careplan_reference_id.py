# Generated by Django 2.1.3 on 2021-08-05 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0077_careplan_cp_pricing_plan_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='careplan',
            name='reference_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
