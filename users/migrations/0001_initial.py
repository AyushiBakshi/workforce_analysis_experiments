# Generated by Django 2.1.3 on 2019-08-14 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_unique_id', models.CharField(blank=True, max_length=128, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('user_name', models.CharField(db_index=True, max_length=45, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('jwt_secret', models.UUIDField(default=uuid.uuid4)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'hcms_um_user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('address_type_mc_id', models.IntegerField(default=99)),
                ('street_1', models.CharField(blank=True, max_length=100, null=True)),
                ('street_2', models.CharField(blank=True, max_length=45, null=True)),
                ('county', models.CharField(blank=True, max_length=45, null=True)),
                ('post_code', models.CharField(blank=True, max_length=45, null=True)),
                ('country', models.CharField(blank=True, max_length=45, null=True)),
                ('telephone_1', models.CharField(blank=True, max_length=45, null=True)),
                ('telephone_2', models.CharField(blank=True, max_length=45, null=True)),
                ('is_mailing_address', models.BooleanField(default=False)),
                ('floor_level', models.SmallIntegerField(blank=True, null=True)),
                ('has_lift', models.IntegerField(blank=True, null=True)),
                ('last_view_addr_type', models.SmallIntegerField(blank=True, null=True)),
                ('main_addr_type', models.SmallIntegerField(blank=True, null=True)),
                ('entry_instructions', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_address',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('alias_id', models.AutoField(primary_key=True, serialize=False)),
                ('title_mc_id', models.IntegerField(blank=True, null=True)),
                ('alias_type_mc_id', models.IntegerField(blank=True, null=True)),
                ('surname', models.CharField(blank=True, max_length=45, null=True)),
                ('forename', models.CharField(blank=True, max_length=45, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_alias',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GeneralPreference',
            fields=[
                ('preference_id', models.IntegerField(primary_key=True, serialize=False)),
                ('preference_type_mc_id', models.IntegerField(blank=True, null=True)),
                ('warns', models.IntegerField(blank=True, null=True)),
                ('parameters', models.CharField(blank=True, max_length=45, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_general_preference',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HcmsUmReview',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('review_type_mc_id', models.IntegerField(blank=True, null=True)),
                ('date_due', models.DateTimeField(blank=True, null=True)),
                ('date_done', models.DateTimeField(blank=True, null=True)),
                ('conducted_by', models.CharField(blank=True, max_length=45, null=True)),
                ('outcome_id', models.IntegerField(blank=True, null=True)),
                ('review_comment', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_review',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HcmsUmRole',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
            ],
            options={
                'db_table': 'hcms_um_role',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ItemAssignedHistory',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('proficiency_mc_id', models.IntegerField(blank=True, null=True)),
                ('assignee_mc_id', models.IntegerField(blank=True, null=True)),
                ('assignment_start', models.DateTimeField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=45, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
            ],
            options={
                'db_table': 'hcms_um_item_assigned_history',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('otp_id', models.AutoField(primary_key=True, serialize=False)),
                ('otp_code', models.IntegerField(blank=True, null=True)),
                ('otp_verification_token', models.UUIDField(default=uuid.uuid4)),
                ('otp_email', models.CharField(blank=True, max_length=255, null=True)),
                ('otp_purpose_mc_id', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
            ],
            options={
                'db_table': 'hcms_um_otp',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('title_mc_id', models.IntegerField(blank=True, null=True)),
                ('sex_mc_id', models.IntegerField(blank=True, null=True)),
                ('mobility_mc_id', models.IntegerField(blank=True, null=True)),
                ('ethnicity_mc_id', models.IntegerField(blank=True, null=True)),
                ('religion_mc_id', models.IntegerField(blank=True, null=True)),
                ('living_circumstances_mc_id', models.IntegerField(blank=True, null=True)),
                ('marital_status_mc_id', models.IntegerField(blank=True, null=True)),
                ('nationality_mc_id', models.IntegerField(blank=True, null=True)),
                ('user_type_mc_id', models.IntegerField(blank=True, null=True)),
                ('forename', models.CharField(blank=True, max_length=45, null=True)),
                ('initials', models.CharField(blank=True, max_length=45, null=True)),
                ('surname', models.CharField(blank=True, max_length=45, null=True)),
                ('is_non_smoker', models.SmallIntegerField(blank=True, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('ni_number', models.CharField(blank=True, max_length=45, null=True)),
                ('fax', models.CharField(blank=True, max_length=45, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('telephone_1', models.CharField(blank=True, max_length=45, null=True)),
                ('telephone_2', models.CharField(blank=True, max_length=45, null=True)),
                ('user_status_mc_id', models.IntegerField(blank=True, null=True)),
                ('profile_image_id', models.IntegerField(blank=True, null=True)),
                ('primary_language_mc_id', models.IntegerField(blank=True, null=True)),
                ('secondary_language_mc_id', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_profile',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PropertyItem',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_type_mc_id', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('date_entered_inventory', models.DateTimeField(blank=True, null=True)),
                ('purchase_price', models.SmallIntegerField(blank=True, null=True)),
                ('initial_location', models.CharField(blank=True, max_length=45, null=True)),
                ('assignment_start_date', models.DateTimeField(blank=True, null=True)),
                ('initial_condition', models.CharField(blank=True, max_length=45, null=True)),
                ('inspector', models.CharField(blank=True, max_length=45, null=True)),
                ('most_recent_inspection', models.DateTimeField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('left_inventory', models.DateTimeField(blank=True, null=True)),
                ('reason_id', models.SmallIntegerField(blank=True, null=True)),
                ('sale_price', models.SmallIntegerField(blank=True, null=True)),
                ('quantity', models.SmallIntegerField(blank=True, null=True)),
                ('reference', models.CharField(blank=True, max_length=50, null=True)),
                ('status_mc_id', models.IntegerField(blank=True, null=True)),
                ('item_given_by', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_property_item',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SameTypePerference',
            fields=[
                ('same_type_preference_id', models.AutoField(primary_key=True, serialize=False)),
                ('other_user_id', models.IntegerField(blank=True, null=True)),
                ('compatibility_mc_id', models.IntegerField(blank=True, null=True)),
                ('no_of_visit', models.SmallIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_same_type_perference',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SpecialPreference',
            fields=[
                ('special_preference_id', models.AutoField(primary_key=True, serialize=False)),
                ('other_user_id', models.IntegerField(blank=True, null=True)),
                ('status_mc_id', models.IntegerField(blank=True, null=True)),
                ('compatibility_mc_id', models.IntegerField(blank=True, null=True)),
                ('no_of_visit', models.SmallIntegerField(blank=True, null=True)),
                ('is_updated', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_special_preference',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserAllocatedBranch',
            fields=[
                ('allocated_branch_id', models.AutoField(primary_key=True, serialize=False)),
                ('branch_mc_id', models.IntegerField(blank=True, null=True)),
                ('unique_key', models.CharField(blank=True, max_length=128, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_allocated_branch', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_allocated_branch',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('language_id', models.AutoField(primary_key=True, serialize=False)),
                ('language_name_mc_id', models.IntegerField(blank=True, null=True)),
                ('proficiency_id', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_language',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('relationship_id', models.AutoField(primary_key=True, serialize=False)),
                ('other_user_id', models.IntegerField(blank=True, null=True)),
                ('other_user_type_mc_id', models.IntegerField(blank=True, null=True)),
                ('status_mc_id', models.IntegerField(blank=True, null=True)),
                ('compatibility_mc_id', models.IntegerField(blank=True, null=True)),
                ('no_of_visit', models.SmallIntegerField(blank=True, null=True)),
                ('updated', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_relationship',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('user_role_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_by', models.IntegerField(blank=True, null=True)),
                ('delete_ind', models.CharField(default='N', max_length=1)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.HcmsUmRole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hcms_um_user_role',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='itemassignedhistory',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.PropertyItem'),
        ),
    ]
