# Generated by Django 2.1.3 on 2020-10-22 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0051_auto_20200910_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingtemplate',
            name='duration',
            field=models.FloatField(default=1, verbose_name='Duration(Days)'),
        ),
    ]