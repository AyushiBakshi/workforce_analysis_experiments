# Generated by Django 2.1.3 on 2020-04-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0044_auto_20200305_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulecr',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
