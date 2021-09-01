# Generated by Django 2.1.3 on 2021-06-29 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0065_auto_20210601_0708'),
        ('booking', '0055_auto_20210512_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='enginerun',
            name='schedule_report',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_report_doc', to='cw.Document'),
        ),
    ]