# Generated by Django 2.1.3 on 2020-10-05 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0049_auto_20200925_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='enginerun',
            name='is_halted',
            field=models.BooleanField(default=False),
        ),
    ]
