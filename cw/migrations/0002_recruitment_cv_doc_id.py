# Generated by Django 2.1.3 on 2019-08-26 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruitment',
            name='cv_doc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]