# Generated by Django 2.1.3 on 2019-10-14 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0003_auto_20191014_0348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='notified',
            new_name='emailed',
        ),
        migrations.RenameField(
            model_name='trigger',
            old_name='notify',
            new_name='email',
        ),
    ]
