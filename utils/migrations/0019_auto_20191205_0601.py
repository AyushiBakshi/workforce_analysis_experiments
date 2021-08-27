# Generated by Django 2.1.3 on 2019-12-05 06:01

from django.db import migrations

addDosageUnits = "BEGIN; \
INSERT INTO public.hcms_utils_master_code ( \
code_id, code_type, code_sub_type, code_no, code_val, code_description, created_date, created_by, last_modified_date, last_modified_by, delete_ind) VALUES ( \
'1112'::integer, 'DOSAGE_UNIT'::character varying(100), ''::character varying(100), '1'::character varying(45), 'ml'::character varying(150), ''::character varying(200), '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, 'N'::character varying(1)) \
 returning code_id; \
INSERT INTO public.hcms_utils_master_code ( \
code_id, code_type, code_sub_type, code_no, code_val, code_description, created_date, created_by, last_modified_date, last_modified_by, delete_ind) VALUES ( \
'1113'::integer, 'DOSAGE_UNIT'::character varying(100), ''::character varying(100), '2'::character varying(45), 'unit'::character varying(150), ''::character varying(200), '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, 'N'::character varying(1)) \
 returning code_id; \
INSERT INTO public.hcms_utils_master_code ( \
code_id, code_type, code_sub_type, code_no, code_val, code_description, created_date, created_by, last_modified_date, last_modified_by, delete_ind) VALUES ( \
'1114'::integer, 'DOSAGE_UNIT'::character varying(100), ''::character varying(100), '3'::character varying(45), 'tbsp'::character varying(150), ''::character varying(200), '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, 'N'::character varying(1)) \
 returning code_id; \
INSERT INTO public.hcms_utils_master_code ( \
code_id, code_type, code_sub_type, code_no, code_val, code_description, created_date, created_by, last_modified_date, last_modified_by, delete_ind) VALUES ( \
'1115'::integer, 'DOSAGE_UNIT'::character varying(100), ''::character varying(100), '4'::character varying(45), 'mg'::character varying(150), ''::character varying(200), '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, '2019-12-05 00:00:00+00'::timestamp with time zone, 1::integer, 'N'::character varying(1)) \
 returning code_id; \
COMMIT;"

class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0018_auto_20191203_0641'),
    ]

    operations = [
        migrations.RunSQL(addDosageUnits)
    ]
