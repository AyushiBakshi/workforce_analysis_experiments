# Generated by Django 2.1.3 on 2019-09-02 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0004_suweeklybooking_candidates'),
    ]

    operations = [
        migrations.AddField(
            model_name='mar',
            name='sequence',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
