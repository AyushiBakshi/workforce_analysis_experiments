# Generated by Django 2.1.3 on 2020-05-13 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0048_auto_20200505_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='medication_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]