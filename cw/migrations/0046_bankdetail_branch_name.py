# Generated by Django 2.1.3 on 2020-06-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0045_auto_20200622_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankdetail',
            name='branch_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
