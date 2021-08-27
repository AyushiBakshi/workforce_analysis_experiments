from django.db import models
from django.utils import timezone
import jwt,uuid
from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser, BaseUserManager,Group
from django_extensions.db.fields import RandomCharField
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField
from dateutil.relativedelta import relativedelta


def return_end_of_time():
    return timezone.now() + relativedelta(years=100)


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="address", on_delete=models.CASCADE)
    address_type_mc_id = models.IntegerField(default=99)
    # property_type_mc_id = models.IntegerField(blank=True, null=True)
    street_1 = models.CharField(max_length=100, blank=True, null=True)
    street_2 = models.CharField(max_length=100, blank=True, null=True)
    # town = models.CharField(max_length=45, blank=True, null=True) # [v2 - removed]
    county = models.CharField(max_length=45, blank=True, null=True)
    post_code = models.CharField(max_length=45)
    country = models.CharField(max_length=45, blank=True, null=True)
    floor_level = models.SmallIntegerField(blank=True, null=True)
    has_lift = models.IntegerField(blank=True, null=True)
    last_view_addr_type = models.SmallIntegerField(blank=True, null=True)
    main_addr_type = models.SmallIntegerField(blank=True, null=True)
    entry_instructions = models.CharField(max_length=1000, blank=True, null=True)
    keysafe_pin = models.CharField(max_length=10, blank=True, null=True) # [v2 - added]
    residence_photos = ArrayField(models.IntegerField(),default=list, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')
    geo_code = models.CharField(blank=True, null=True, max_length=100)
    traveltime_generated = models.CharField(max_length=1, default='N')
    is_add_outside_business_boundary = models.CharField(max_length=1, default='N')
    contact_post_code = models.CharField(max_length=45, blank=True, null=True, default=None)
    effective_from = models.DateTimeField(blank=True, null=True)
    effective_until = models.DateTimeField(blank=True, null=True, default = datetime.max.replace(tzinfo=timezone.utc))
    bookings_handled = models.BooleanField(default=True)
    handle_bookings_until = models.DateTimeField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)
    restore_from = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hcms_um_address'

    def adjust_effective_until(old_address_id, effective_from):
        effective_until_adjusted = effective_from - timedelta(microseconds=1000)
        address = Address.objects.filter(pk=old_address_id).first()
        if address.handle_bookings_until:
            address.handle_bookings_until = min(address.handle_bookings_until, effective_until_adjusted)
        address.effective_until = effective_until_adjusted
        address.save()

    def get_valid_address_id_for_time(start_time, user_id):
        valid_address = Address.objects.filter(user_id=user_id, effective_from__lte=start_time,
                                               effective_until__gt=start_time, is_cancelled=False).first()

        return valid_address.address_id if valid_address else None




class Alias(models.Model):
    alias_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title_mc_id = models.IntegerField(blank=True, null=True)
    alias_type_mc_id = models.IntegerField(blank=True, null=True)
    surname = models.CharField(max_length=45, blank=True, null=True)
    forename = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_alias'


# class ContactPerson(models.Model):
#     contact_person_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     contact_type_mc_id = models.IntegerField(blank=True, null=True)
#     start_date = models.DateTimeField(blank=True, null=True)
#     finished_date = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=200, blank=True, null=True)
#     created_date = models.DateTimeField(default=timezone.now)
#     created_by = models.IntegerField(blank=True, null=True)
#     last_modified_date = models.DateTimeField(default=timezone.now)
#     last_modified_by = models.IntegerField(blank=True, null=True)
#     delete_ind = models.CharField(max_length=1, default='N')
#
#     class Meta:
#         managed = True
#         db_table = 'hcms_um_contact_person'


class SpecialPreference(models.Model):
    special_preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    other_user_id = models.IntegerField(blank=True, null=True)
    status_mc_id = models.IntegerField(blank=True, null=True)
    compatibility_mc_id = models.IntegerField(blank=True, null=True)
    no_of_visit = models.SmallIntegerField(blank=True, null=True)
    is_updated = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_special_preference'


class GeneralPreference(models.Model):
    preference_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    preference_type_mc_id = models.IntegerField(blank=True, null=True)
    warns = models.IntegerField(blank=True, null=True)
    parameters = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_general_preference'


class ItemAssignedHistory(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('PropertyItem', on_delete=models.CASCADE)
    proficiency_mc_id = models.IntegerField(blank=True, null=True)
    assignee_mc_id = models.IntegerField(blank=True, null=True)
    assignment_start = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_item_assigned_history'

# class Journal(models.Model):
#     journal_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     title = models.CharField(max_length=200, blank=True, null=True)
#     journal_type_mc_id = models.IntegerField(blank=True, null=True)
#     note = models.TextField(blank=True, null=True)
#     file_path = models.CharField(max_length=200, blank=True, null=True)
#     created_date = models.DateTimeField(default=timezone.now)
#     created_by = models.IntegerField(blank=True, null=True)
#     last_modified_date = models.DateTimeField(default=timezone.now)
#     last_modified_by = models.IntegerField(blank=True, null=True)
#     delete_ind = models.CharField(max_length=1, default='N')
#
#     class Meta:
#         managed = True
#         db_table = 'hcms_um_journal'


class UserLanguage(models.Model):
    language_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name="language", on_delete=models.CASCADE)
    language_name_mc_id = models.IntegerField(blank=True, null=True)
    proficiency_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_language'

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<user_id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.user_id, filename)

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="profile", on_delete=models.CASCADE)
    title_mc_id = models.IntegerField(blank=True, null=True)
    sex_mc_id = models.IntegerField(blank=True, null=True)
    # service_user_type_mc_id = models.IntegerField(blank=True, null=True)
    mobility_mc_id = models.IntegerField(blank=True, null=True)
    ethnicity_mc_id = models.IntegerField(blank=True, null=True)
    religion_mc_id = models.IntegerField(blank=True, null=True)
    living_circumstances_mc_id = models.IntegerField(blank=True, null=True)
    marital_status_mc_id = models.IntegerField(blank=True, null=True)
    user_type_mc_id = models.IntegerField(blank=True, null=True)
    forename = models.CharField(max_length=50, blank=True, null=True)
    initials = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    is_non_smoker = models.SmallIntegerField(blank=True, null=True) # [v3 - added]
    dob = models.DateTimeField(blank=True, null=True)
    ni_number = models.CharField(max_length=9, blank=True, null=True)
    nhs_no = models.CharField(max_length=12, blank=True, null=True) # [v3 - added]
    fax = models.CharField(max_length=45, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    telephone_1 = models.CharField(max_length=15, blank=True, null=True) # [v4 - added]
    telephone_2 = models.CharField(max_length=15, blank=True, null=True) # [v4 - added]
    user_status_mc_id = models.IntegerField(blank=True, null=True) # active, pending, terminated
    profile_image_id = models.IntegerField(blank=True, null=True)  # [v2 - added]
    primary_language_mc_id = models.IntegerField(blank=True, null=True) # [v2 - added] # [v3 - added]
    secondary_language_mc_id = models.IntegerField(blank=True, null=True) # [v2 - added] # [v3 - added]
    misc_info = models.TextField(blank=True, null=True)

    contact = models.ManyToManyField('users.Contact',related_name="user_contacts", blank=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_profile'


class PropertyItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item_type_mc_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    date_entered_inventory = models.DateTimeField(blank=True, null=True)
    purchase_price = models.SmallIntegerField(blank=True, null=True)
    initial_location = models.CharField(max_length=45, blank=True, null=True)
    assignment_start_date = models.DateTimeField(blank=True, null=True)
    initial_condition = models.CharField(max_length=45, blank=True, null=True)
    inspector = models.CharField(max_length=45, blank=True, null=True)
    most_recent_inspection = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    left_inventory = models.DateTimeField(blank=True, null=True)
    reason_id = models.SmallIntegerField(blank=True, null=True)
    sale_price = models.SmallIntegerField(blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    status_mc_id = models.IntegerField(blank=True, null=True)
    item_given_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_property_item'


class UserRelationship(models.Model):
    relationship_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    other_user_id = models.IntegerField(blank=True, null=True)
    other_user_type_mc_id = models.IntegerField(blank=True, null=True)
    status_mc_id = models.IntegerField(blank=True, null=True)
    compatibility_mc_id = models.IntegerField(blank=True, null=True)
    no_of_visit = models.SmallIntegerField(blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_relationship'


class HcmsUmReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    review_type_mc_id = models.IntegerField(blank=True, null=True)
    date_due = models.DateTimeField(blank=True, null=True)
    date_done = models.DateTimeField(blank=True, null=True)
    conducted_by = models.CharField(max_length=45, blank=True, null=True)
    outcome_id = models.IntegerField(blank=True, null=True)
    review_comment = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_review'


class HcmsUmRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_role'


class SameTypePerference(models.Model):
    same_type_preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    other_user_id = models.IntegerField(blank=True, null=True)
    compatibility_mc_id = models.IntegerField(blank=True, null=True)
    no_of_visit = models.SmallIntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_same_type_perference'


class UserManager(BaseUserManager):
    def create_user(self, email, password, group, created_by, is_active=False, is_staff=False,
                    is_superuser=False):

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password.')
        if not group:
            raise serializers.ValidationError(
                'Users must have a group.'
            )

        ex_group = Group.objects.get(name = group)
        if ex_group is None:
            raise serializers.ValidationError(
                'Invalid group.'
            )

        user = self.model(
            email=self.normalize_email(email),
            is_active = is_active,
            is_staff = is_staff,
            created_by=created_by,
            is_superuser=is_superuser,
            last_modified_by=created_by
        )

        user.set_password(password)
        user.save()
        ex_group.user_set.add(user)

        return user

    def create_superuser(self, user_name, email, password):
        if user_name is None:
            raise TypeError('Users must have a user_name.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(user_name=user_name,
            email=self.normalize_email(email),
            created_by=None,
            last_modified_by=None
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()


        return user


# class User(models.Model):
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_unique_id = models.CharField(max_length=128, blank=True, null=True) # userID
    email = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # user_name = models.CharField(max_length=45, blank=True, null=True)
    user_name = RandomCharField(length=8, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    channel_name = models.CharField(max_length=256, blank=True, null=True)
    jwt_secret = models.UUIDField(default=uuid.uuid4)
    last_activity = models.DateTimeField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    SHORT_NAMES = {
            'Care Worker':'CW',
            'Coordinator':'CTR',
            'Finance':'FIN',
            'HR':'HR',
            'Management':'MGT',
            'Service User':'SU',
            'Supervisor':'SUP',
            'System':'SYS'
        }
    objects = UserManager()

    def __str__(self):
        return self.user_name

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def group(self):
        groups=self.groups.all()
        if groups:
            return groups[0].name
        return ""

    @property
    def group_short(self):
        return User.SHORT_NAMES.get(self.group,"")

    @property
    def group_id(self):
        groups=self.groups.all()
        if groups:
            return groups[0].id
        return -1

    def get_full_name(self):
        first_name = self.profile.forename
        middle_name = self.profile.middle_name if self.profile.middle_name else ''
        last_name = self.profile.surname
        name = '%s %s %s' % (first_name, middle_name, last_name)
        return name

    def get_short_name(self):
        return self.user_name

    def set_active(self,is_active):
        self.is_active = is_active
        self.save()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'id': self.pk,
            'secret': str(self.jwt_secret),
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def set_channel(self,channel):
        self.channel_name = channel
        self.save()

    class Meta:
        managed = True
        db_table = 'hcms_um_user'



class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(HcmsUmRole, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_user_role'


class UserAllocatedBranch(models.Model):
    allocated_branch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="user_allocated_branch", on_delete=models.CASCADE)
    branch_mc_id = models.IntegerField(blank=True, null=True)
    unique_key = models.CharField(max_length=128, blank=True, null=True)  # random number, unique
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_allocated_branch'

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=100)
    email = models.CharField(blank=True, null=True,max_length=255)
    contact_type_mc_id = models.IntegerField(blank=True, null=True)
    is_emergency_contact = models.BooleanField(default=False) # [v3 - added]
    is_private = models.BooleanField(default=False) # [v3 - added]

    street_1 = models.CharField(max_length=100, blank=True, null=True)
    street_2 = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=45, blank=True, null=True)
    telephone_1 = models.CharField(max_length=15, blank=False, null=False)
    telephone_2 = models.CharField(max_length=15, blank=True, null=True)
    send_email = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_contact'

from django.contrib.postgres.fields import ArrayField
from utils.models import Data
class Reminder(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    requested_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="reminder_caller",blank=True, null=True)
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="reminder_actor",blank=True, null=True)
    origin = models.ForeignKey('self', on_delete=models.CASCADE, related_name="reminder_origin",blank=True, null=True)
    original_reminder = models.ForeignKey('self', on_delete=models.CASCADE, related_name="reminder_original_req",blank=True, null=True)
    reminder_status_mc_id = models.IntegerField(blank=True, null=True) #REMINDER_STATUS;
    subject = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    admin_remark = models.TextField(blank=True, null=True)
    respond_by = models.DateTimeField(blank=True, null=True)
    attachments = ArrayField(models.CharField(max_length=100),default=list)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="reminder_receiver") #service user
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_um_reminder'

    def set_resolved(self):
        RESOLVED = Data.code('REMINDER_STATUS','Resolved')
        self.reminder_status_mc_id = Reminder.RESOLVED
        self.save()

    def forward(self,created_by_id, receipient_id,admin_remark,attachments):

        PENDING = Data.code('REMINDER_STATUS','Pending')
        FORWARDED = Data.code('REMINDER_STATUS','Forwarded')
        self.reminder_status_mc_id = FORWARDED
        self.last_modified_date = timezone.now()
        self.last_modified_by = created_by_id
        self.save()

        self.created_by_id =  created_by_id
        self.created_date = timezone.now()
        self.last_modified_date = timezone.now()
        self.last_modified_by = created_by_id
        self.recipient_id = receipient_id
        self.subject = self.subject
        self.origin_id = self.reminder_id
        self.original_reminder = self.original_reminder
        self.reminder_status_mc_id = PENDING
        self.admin_remark = admin_remark
        self.attachments = attachments
        self.pk = None
        self.save()
        return self

    def resolve(self,requested_by,admin_remark,attachments):
        self.reminder_status_mc_id = Data.code('REMINDER_STATUS','Resolved')
        self.last_modified_date = timezone.now()
        self.last_modified_by = requested_by
        self.original_reminder = self.original_reminder
        self.admin_remark = admin_remark
        self.attachments = attachments
        self.save()
        return self

    def acknowledge(self):
        self.reminder_status_mc_id = Data.code('REMINDER_STATUS', 'Acknowledgement')
        self.last_modified_date = timezone.now()
        self.created_date = timezone.now()
        self.last_modified_by = User.objects.get(user_name='sys').user_id
        self.created_by_id = User.objects.get(user_name='sys').user_id
        self.recipient = self.requested_by
        self.subject = self.subject
        self.origin_id = self.reminder_id
        self.original_reminder = self.original_reminder
        self.admin_remark = self.admin_remark
        self.attachments = self.attachments
        self.pk = None
        self.save()
        return self


from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
import json

class Log(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="user_log",blank=True, null=True)
    record_id = models.IntegerField(blank=True, null=True)
    log_type = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    content = JSONField(default=dict)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="log_creator") #service user

    class Meta:
        managed = True
        db_table = 'hcms_um_log'

    def create(user,log_type,content,created_by,record_id=None):
        def default(o):
            if type(o) is datetime:
                return o.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        content_json = json.loads(json.dumps(content, default=default))

        return Log.objects.create(
                user = user,
                log_type = log_type,
                content =  content_json,
                record_id=record_id,
                created_by = created_by,
            )


from django.contrib.postgres.fields import ArrayField
class UserAdminAccess(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    last_modified_date = models.DateTimeField(default=timezone.now, verbose_name="Last Modified On")
    last_modified_by = models.ForeignKey('users.User', on_delete=models.CASCADE,blank=True, null=True, verbose_name="Last Modified By")
    users_selected = ArrayField(models.CharField(max_length=2000, blank=True, null=True, verbose_name="Users Selected"), blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")
    remarks = models.CharField(max_length=200, blank=True, null=True, verbose_name='Remarks')

    class Meta:
        managed = True
        db_table = 'hcms_um_user_admin_access'
