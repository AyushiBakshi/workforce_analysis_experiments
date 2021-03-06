# Generated by Django 2.1.3 on 2020-09-10 01:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0050_auto_20200909_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingtemplate',
            name='items_covered',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('Administer Syringe', 'Administer Syringe'), ('Urinary Catheter Insertion', 'Urinary Catheter Insertion'), ('Stroke Care', 'Stroke Care'), ('OCD Awareness', 'OCD Awareness'), ('Incontinence and Continence care', 'Incontinence and Continence care'), ('Emergency first Aid level 2', 'Emergency first Aid level 2'), ('First Aid level 3', 'First Aid level 3'), ('Falls Prevention', 'Falls Prevention'), ('Peck Feeding', 'Peck Feeding'), ('Stoma Care', 'Stoma Care'), ('Palliative and End-of-life care', 'Palliative and End-of-life care'), ('Catheter care', 'Catheter care'), ('Epilepsy awareness', 'Epilepsy awareness'), ('Dementia Awareness', 'Dementia Awareness'), ('Stroke Care', 'Stroke Care'), ('Diabetes Awareness', 'Diabetes Awareness'), ('Understanding Eating Disorders', 'Understanding Eating Disorders'), ('Autism Introduction courses', 'Autism Introduction courses'), ('Learning Disability awareness', 'Learning Disability awareness'), ('Multiple Sclerosis training', 'Multiple Sclerosis training'), ('Asperger’s awareness course', 'Asperger’s awareness course'), ('Arthritis Care', 'Arthritis Care'), ('Tourette’s syndrome assistance', 'Tourette’s syndrome assistance'), ('Visual and Hearing Impairment care', 'Visual and Hearing Impairment care'), ('Supporting Children with Disabilities', 'Supporting Children with Disabilities'), ('Bipolar Awareness', 'Bipolar Awareness'), ('Schizophrenia Awareness', 'Schizophrenia Awareness'), ('OCD Awareness', 'OCD Awareness'), ('Self-Harm Awareness', 'Self-Harm Awareness'), ('Borderline Personality Disorder Awareness', 'Borderline Personality Disorder Awareness'), ('NVQ level 2', 'NVQ level 2'), ('NVQ Level 3', 'NVQ Level 3'), ('NVQ Level 1', 'NVQ Level 1'), ('NVQ Level 4', 'NVQ Level 4'), ('NVQ Level 5', 'NVQ Level 5'), ('Fluids and Nutrition', 'Fluids and Nutrition'), ('Safeguarding Adults', 'Safeguarding Adults'), ('Safeguarding Children', 'Safeguarding Children'), ('Basic Life Support/First Aid', 'Basic Life Support/First Aid'), ('Health and Safety', 'Health and Safety'), ('Moving & Handling', 'Moving & Handling'), ('Infection control and prevention/Hygiene', 'Infection control and prevention/Hygiene'), ('Medication Administration', 'Medication Administration'), ('Food Hygiene', 'Food Hygiene'), ('Understand your role', 'Understand your role'), ('Your Personal Development', 'Your Personal Development'), ('Duty of Care', 'Duty of Care'), ('Equality, Diversity & Inclusion', 'Equality, Diversity & Inclusion'), ('Work in a Person Centred Way', 'Work in a Person Centred Way'), ('Effective Communication', 'Effective Communication'), ('Privacy and Dignity', 'Privacy and Dignity'), ('Managing Challenging Behaviour', 'Managing Challenging Behaviour'), ('Raising concerns & Whistle blowing', 'Raising concerns & Whistle blowing'), ('Awareness of Mental Health/Learning Disabilities', 'Awareness of Mental Health/Learning Disabilities'), ('Incontinence and Continence care', 'Incontinence and Continence care'), ('Mandatory Induction Training - Part A', 'Mandatory Induction Training - Part A'), ('Mandatory Induction Training - Part B', 'Mandatory Induction Training - Part B')], max_length=2000, null=True), size=None),
        ),
    ]
