# Generated by Django 2.1.3 on 2019-12-05 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('su', '0032_auto_20191204_0614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactaddress',
            name='contact_person',
        ),
        migrations.RemoveField(
            model_name='sucontactperson',
            name='user',
        ),
        migrations.DeleteModel(
            name='ContactAddress',
        ),
        migrations.DeleteModel(
            name='SuContactPerson',
        ),
    ]
