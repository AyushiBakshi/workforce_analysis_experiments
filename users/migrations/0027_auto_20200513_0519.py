# Generated by Django 2.1.3 on 2020-05-13 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_profile_nhs_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='keysafe_pin',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='contact_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='street_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='telephone_1',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='contact',
            name='telephone_2',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='forename',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='initials',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nhs_no',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ni_number',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='surname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telephone_1',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telephone_2',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
