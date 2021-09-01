# Generated by Django 2.1.3 on 2020-09-03 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0062_cwexception_is_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalhistory',
            name='proof_doc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medication',
            name='proof_doc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]