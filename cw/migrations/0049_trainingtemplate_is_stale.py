# Generated by Django 2.1.3 on 2020-09-08 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0048_auto_20200908_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingtemplate',
            name='is_stale',
            field=models.BooleanField(default=False, verbose_name='Mark As Stale'),
        ),
    ]
