# Generated by Django 2.1.3 on 2021-05-10 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0062_auto_20210510_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='file',
        ),
    ]
