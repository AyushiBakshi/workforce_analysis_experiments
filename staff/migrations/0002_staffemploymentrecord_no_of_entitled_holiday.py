# Generated by Django 2.1.3 on 2019-09-03 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffemploymentrecord',
            name='no_of_entitled_holiday',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
