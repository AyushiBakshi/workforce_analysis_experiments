# Generated by Django 2.1.3 on 2019-12-10 07:46

from django.db import migrations

updatePayFrequency = "\
BEGIN; \
UPDATE public.hcms_utils_master_code SET \
code_val = 'Hourly'::character varying(150), last_modified_date = '2019-12-10 00:07:46+00'::timestamp with time zone WHERE \
code_id = 1097; \
COMMIT;"

reversePayFrequency = "\
BEGIN; \
UPDATE public.hcms_utils_master_code SET \
code_val = 'Weekly'::character varying(150), last_modified_date = '2019-12-10 00:07:46+00'::timestamp with time zone WHERE \
code_id = 1097; \
COMMIT;"

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0021_auto_20191206_0218'),
    ]

    operations = [
        migrations.RunSQL(updatePayFrequency, reversePayFrequency)
    ]
