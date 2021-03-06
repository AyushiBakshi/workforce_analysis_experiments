# Generated by Django 2.1.3 on 2020-08-08 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0035_traveltimecoordinatesavehistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traveltimecoordinatesavehistory',
            old_name='save_error',
            new_name='excluded_users_error',
        ),
        migrations.RemoveField(
            model_name='traveltimecoordinatesavehistory',
            name='save_status',
        ),
        migrations.AddField(
            model_name='traveltimecoordinatesavehistory',
            name='excluded_users_status',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='traveltimecoordinatesavehistory',
            name='new_coordinates',
            field=models.TextField(),
        ),
    ]
