# Generated by Django 2.1.3 on 2020-04-01 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_reminder_admin_remarks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reminder',
            old_name='admin_remarks',
            new_name='admin_remark',
        ),
    ]