# Generated by Django 2.1.3 on 2020-05-14 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0049_auto_20200513_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceuser',
            name='has_no_pets',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
