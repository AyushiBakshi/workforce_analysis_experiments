# Generated by Django 2.1.3 on 2020-08-08 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0037_auto_20200808_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='traveltimerelatedprocesses',
            name='show_text_box',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
