# Generated by Django 2.1.3 on 2019-08-21 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_hcmsconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hcmsconfig',
            name='code_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
