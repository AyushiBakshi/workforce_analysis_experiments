# Generated by Django 2.1.3 on 2020-05-05 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0047_auto_20200504_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulecr',
            name='reason',
            field=models.TextField(blank=True),
        ),
    ]
