# Generated by Django 2.1.3 on 2020-12-04 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0047_auto_20201029_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderConfig',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('utils.hcmsconfig',),
        ),
    ]
