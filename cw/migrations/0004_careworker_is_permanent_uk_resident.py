# Generated by Django 2.1.3 on 2019-08-26 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0003_employmentrecord_job_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='careworker',
            name='is_permanent_uk_resident',
            field=models.BooleanField(default=False),
        ),
    ]