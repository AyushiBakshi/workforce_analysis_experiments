# Generated by Django 2.1.3 on 2019-11-11 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0018_auto_20191111_0759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suweeklybooking',
            old_name='funding_type_mc_id',
            new_name='care_plan_id',
        ),
        migrations.RemoveField(
            model_name='suweeklybooking',
            name='change_requests',
        ),
        migrations.AddField(
            model_name='suweeklybooking',
            name='cr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='suweeklybooking',
            name='unique_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
