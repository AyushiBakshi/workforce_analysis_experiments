# Generated by Django 2.1.3 on 2020-05-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20200514_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_non_smoker',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
