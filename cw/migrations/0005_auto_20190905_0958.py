# Generated by Django 2.1.3 on 2019-09-05 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0004_careworker_is_permanent_uk_resident'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document', to=settings.AUTH_USER_MODEL),
        ),
    ]