# Generated by Django 2.1.3 on 2019-11-15 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0011_traveltimegenerationhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traveltimegenerationhistory',
            old_name='import_nodes_id',
            new_name='import_nodes',
        ),
        migrations.RenameField(
            model_name='traveltimegenerationhistory',
            old_name='map_id',
            new_name='map',
        ),
        migrations.RenameField(
            model_name='ImportNodesRunHistory',
            old_name='map_id',
            new_name='map',
        ),
    ]
