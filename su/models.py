from django.db import models
from django.utils import timezone
import json

from channel.sync import notify_to_sync
from users.models import (
   User
)
from django.db.models import Q
from pytz import tzinfo
from utils.models import Data
import datetime
from django.contrib.postgres.fields import ArrayField



class ServiceUser(models.Model):
    service_user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="serviceuser", on_delete=models.CASCADE)
    referred_status_mc_id = models.IntegerField(blank=True, null=True)
    service_contract_mc_id = models.IntegerField(blank=True, null=True)
    reason_finished_id = models.IntegerField(blank=True, null=True)
    band_mc_id = models.IntegerField(blank=True, null=True)
    team_mc_id = models.IntegerField(blank=True, null=True)
    sector_mc_id = models.IntegerField(blank=True, null=True)
    contract_mc_id = models.IntegerField(blank=True, null=True)
    date_referred = models.DateTimeField(blank=True, null=True)
    referred_by = models.IntegerField(blank=True, null=True)
    date_referral = models.DateTimeField(blank=True, null=True)
    referral_ref_code = models.CharField(max_length=45, blank=True, null=True)
    planned_start_date = models.DateTimeField(blank=True, null=True)
    service_start_date = models.DateTimeField(blank=True, null=True)
    service_finish_date = models.DateTimeField(blank=True, null=True)
    externally_involved = models.IntegerField(blank=True, null=True)
    has_no_pets = models.SmallIntegerField(blank=True, null=True) # [v3 - added]
    service_user_type_mc_id = models.IntegerField(blank=True, null=True) #[v4 - added] #SERVICE_USER_TYPE Private, Public
    su_status_mc_id = models.IntegerField(blank=True, null=True)  # [v2 - added]
    medical_status_note = models.CharField(max_length=200, blank=True, null=True) # [v2 - added]

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_service_user'

    @property
    def exceptions(self):
        ex = CWException.objects.filter(user = self.user,is_current=True).first()
        return ex.exceptions if ex else ""

class CWException(models.Model):
    cw_exception_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="cw_exceptions", on_delete=models.CASCADE)
    exceptions = models.TextField(blank=True,null=True) #comma sperated username list
    is_current = models.BooleanField(default=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_cw_exception'



class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="comment", on_delete=models.CASCADE)
    is_complex_package = models.BooleanField(default=False)
    warning_message = models.TextField(blank=True, null=True)
    is_displayed = models.BooleanField(default=False)
    roster_comment = models.TextField(blank=True, null=True)
    background_comment = models.TextField(blank=True, null=True)
    reason_mc_id = models.IntegerField(blank=True, null=True)
    is_complex_package = models.BooleanField(default=False)
    note = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_comment'


class Compliance(models.Model):
    compliance_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="compliance", on_delete=models.CASCADE)
    is_daily_comment_sheet = models.BooleanField(default=False)
    is_mar_chart = models.BooleanField(default=False)
    is_financial_transaction = models.BooleanField(default=False)
    note = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_compliance'


class FundingDetail(models.Model):
    funding_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    funder_name = models.CharField(max_length=45, blank=True, null=True)
    arrangement = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_funding_detail'


class MedicalHistory(models.Model):
    medical_history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="medical_history", on_delete=models.CASCADE)
    # condition_type_mc_id = models.IntegerField(blank=True, null=True)
    condition_type = models.CharField(max_length=100, blank=True, null=True)
    treatment_status_mc_id = models.IntegerField(blank=True, null=True)
    severity_mc_id = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
    proof_doc_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_medical_history'


class MentalCapacity(models.Model):
    mental_capacity_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="mental_capacity", on_delete=models.CASCADE)
    mental_capacity_mc_id = models.IntegerField(blank=True, null=True)
    reason_mc_id = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_mental_capacity'


class PurchaseOrder(models.Model):
    purchase_order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    cover_type_mc_id = models.IntegerField(blank=True, null=True)
    type_of_service_mc_id = models.IntegerField(blank=True, null=True)
    package_type_mc_id = models.IntegerField(blank=True, null=True)
    funder_name_mc_id = models.IntegerField(blank=True, null=True)
    po_number = models.CharField(max_length=200, blank=True, null=True)
    service_start_date = models.DateTimeField(blank=True, null=True)
    service_start_time_mc_id = models.IntegerField(blank=True, null=True)
    no_of_weekly_hours = models.SmallIntegerField(blank=True, null=True)
    service_end_date = models.DateTimeField(blank=True, null=True)
    is_attention_required = models.BooleanField(default=False)
    note = models.CharField(max_length=200, blank=True, null=True)
    status_mc_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_purchase_order'


class Responsibility(models.Model):
    responsibility_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="responsibility", on_delete=models.CASCADE)
    key_worker_mc_id = models.IntegerField(blank=True, null=True)
    key_administrator_mc_id = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_responsibility'


class ServiceTermination(models.Model):
    service_termination_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="service_termination", on_delete=models.CASCADE)
    is_terminated_service = models.BooleanField(default=False)
    terminated_date = models.DateTimeField(blank=True, null=True)
    last_call_covered_mc_id = models.IntegerField(blank=True, null=True)
    reason_mc_id = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    signed_off_by = models.IntegerField(blank=True, null=True)
    signed_off_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_service_termination'


class HcmsSuPreference(models.Model):
    su_preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="su_preference", on_delete=models.CASCADE)  # service user
    # unique_key = models.CharField(max_length=128, blank=True, null=True)  # random number, unique
    preference_type_mc_id = models.IntegerField(blank=True, null=True)
    # preference_value_mc_id = models.IntegerField(blank=True, null=True)
    preference_value = models.CharField(max_length=200, blank=True, null=True)  # id(s) only, "1, 2, 3, ..."" # [v2 - added]
    incorporation_type_mc_id = models.IntegerField(blank=True, null=True)  # soft, hard, not specified
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_preference'


class HcmsSuCwpreference(models.Model):
    id = models.IntegerField(primary_key=True)
    su = models.ForeignKey('su.ServiceUser', on_delete=models.CASCADE)
    cw = models.ForeignKey('cw.CareWorker', on_delete=models.CASCADE)
    rank = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_cw_preference'


# class SuAllocatedBranch(models.Model):
#     allocated_branch_id = models.AutoField(primary_key=True)
#     user = models.OneToOneField('users.User', related_name="su_allocated_branch", on_delete=models.CASCADE)
#     sector_mc_id = models.IntegerField(blank=True, null=True)
#     branch_mc_id = models.IntegerField(blank=True, null=True) # team
#     zone_mc_id = models.IntegerField(blank=True, null=True)
#     note = models.CharField(max_length=200, blank=True, null=True)
#     created_date = models.DateTimeField(default=timezone.now)
#     created_by = models.IntegerField(blank=True, null=True)
#     last_modified_date = models.DateTimeField(default=timezone.now)
#     last_modified_by = models.IntegerField(blank=True, null=True)
#     delete_ind = models.CharField(max_length=1, default='N')
#
#     class Meta:
#         managed = True
#         db_table = 'hcms_su_allocated_branch'


class ServiceStatus(models.Model):
    service_status_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="service_status", on_delete=models.CASCADE)
    is_start_provided_service = models.BooleanField(default=False)
    service_start_date = models.DateTimeField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    signed_off_by = models.IntegerField(blank=True, null=True)
    signed_off_date = models.DateTimeField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_service_status'


class Audit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="audit", on_delete=models.CASCADE)
    audit_type_mc_id = models.IntegerField(blank=True, null=True)
    month_year = models.DateTimeField(blank=True, null=True) # June-2017
    document_date = models.DateTimeField(blank=True, null=True)
    document_brought_by = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    is_action_taken = models.BooleanField(default=False)
    outcome = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_audit'


# class SuScheduledBooking(models.Model):
#     su_scheduled_booking_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="su_scheduled_booking") #service user
#     booking_type_mc_id = models.IntegerField(blank=True, null=True)
#     day_of_the_week = models.IntegerField(blank=True, null=True)  # MON, TUE, WED ....
#     start_time = models.TimeField(blank=True, null=True)
#     end_time = models.TimeField(blank=True, null=True)
#     no_of_cw = models.SmallIntegerField(blank=True, null=True)
#     created_date = models.DateTimeField(default=timezone.now)
#     created_by = models.IntegerField(blank=True, null=True)
#     last_modified_date = models.DateTimeField(default=timezone.now)
#     last_modified_by = models.IntegerField(blank=True, null=True)
#     delete_ind = models.CharField(max_length=1, default='N')
#
#     class Meta:
#         managed = True
#         db_table = 'hcms_su_scheduled_booking'


class SuBookingSchedule(models.Model):
    booking_schedule_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="su_booking_schedule") #service user
    booking_schedule_status_mc_id = models.IntegerField(blank=True, null=True) #Current, Historic

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_booking_schedule'

from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
import copy
from booking.models import BookingChangeRequest, ScheduledBooking, TaskTemplate, BookingHistory, EngineRun


import operator
from functools import reduce
from django.db.models import F, Func
class SuWeeklyBooking(models.Model):
    weekly_booking_id = models.AutoField(primary_key=True)
    service_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="su_weekly_bookings") #service user
    booking_type_mc_id = models.IntegerField(blank=True, null=True)
    day_of_the_week = models.SmallIntegerField(blank=True, null=True)  # MON, TUE, WED ....
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    no_of_cw = models.SmallIntegerField(blank=True, null=True)
    medications = JSONField(blank=True, null=True)
    tasks = JSONField(blank=True, null=True)
    consumables = JSONField(blank=True, null=True)

    frequency = models.IntegerField(default=1) # [v3 - added]
    freq_ref_date = models.DateTimeField(blank=True, null=True)
    is_critical = models.BooleanField(default=False)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    care_plan_id = models.IntegerField(blank=True, null=True)
    cr = models.IntegerField(blank=True, null=True)
    unique_link = models.TextField(blank=True, null=True)

    skills_required = ArrayField(models.IntegerField(),default=list)

    notes = models.TextField(blank=True, null=True)
    fixed_cws = ArrayField(models.CharField(max_length=100),default=list,blank=True, null=True)
    fixed_cws_modified_date = models.DateTimeField(blank=True, null=True)
    b_gen_comment = JSONField(default=list)
    candidates = JSONField(blank=True, null=True) #{"scores": {"9": 5.0,...}, "allocated_cws": {"17": 3.33, "19": 3.33}}

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_weekly_booking'


from django.contrib.postgres.fields import JSONField
class ScheduleCR(models.Model):
    schedule_change_request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="su_schedule_reqs") #service user
    effective_from = models.DateTimeField(blank=True, null=True)
    effective_to = models.DateTimeField(blank=True, null=True)
    change_type_mc_id = models.IntegerField(blank=True, null=True)
    scr_event_type_mc_id = models.IntegerField(blank=True, null=True) #SCR_EVENT_TYPE:Booking Adjustment,Missed Booking,Initial Change, Service User Request, Authority Request
    related_id = models.IntegerField(blank=True, null=True)
    reason = models.TextField(blank=True,null=True)
    changes = JSONField(default = list)
    weekly_booking = JSONField(default = list)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_schedule_cr'


class SuJournal(models.Model):
    su_journal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="su_journal") #service user
    journal_type_mc_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_journal'


class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="medication") #service user
    condition_type_mc_id = models.IntegerField(blank=True, null=True)
    medication_type_mc_id = models.IntegerField(blank=False, null=False)
    medication_status_mc_id = models.IntegerField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    # note = models.TextField(blank=True, null=True)

    # medication_name_mc_id = models.IntegerField(blank=False, null=False) # [v3 - added]
    medication_name = models.CharField(max_length=50, blank=True, null=True) # [v4 - edited]
    strength = models.CharField(max_length=50) # [v4 - edited]
    administration_details = models.TextField(blank=True, null=True) # [v3 - added]
    warnings = models.TextField(blank=True, null=True) # [v3 - added]
    medication_doc_id = models.IntegerField(blank=True, null=True) # [v3 - added]
    proof_doc_id = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    dosage_unit_mc_id = models.IntegerField(blank=True, null=True) # [v3 - added]
    dosage = models.IntegerField(blank=True, null=True) # [v3 - added]
    slots = JSONField(blank=True, null=True)
    weekdays = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    terminated_on = models.DateTimeField(blank=True, null=True)
    termination_proof_doc_id = models.IntegerField(blank=True, null=True)
    termination_remark = models.TextField(blank=True, null=True) # [v3 - added]
    meal_preference_mc_id = models.IntegerField(blank=True, null=True)


    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_medication'


class CarePlan(models.Model): # [v4 - added]
    care_plan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="care_plan")  # service user

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    termination_date = models.DateTimeField(blank=True, null=True)
    termination_attachment = models.IntegerField(blank=True, null=True)
    termination_notes = models.TextField(blank=True, null=True)

    funding_type_mc_id = models.IntegerField(blank=True, null=True)
    funding_sub_type_mc_id = models.IntegerField(blank=True, null=True)
    reference_id = models.CharField(blank=True, max_length=200, null=True)

    support_plan_doc_id = models.IntegerField(blank=True, null=True)
    cp_pricing_plan_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_care_plan'


class Mar(models.Model): # Medical Administration Record, [v4 - added]
    mar_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('booking.ScheduledBooking', on_delete=models.CASCADE, related_name="mar")
    medication_id = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    is_administered = models.BooleanField(default=False)
    administered_by = models.IntegerField(blank=True, null=True)
    administered_time = models.DateTimeField(blank=True, null=True)


    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_mar'

class Observation(models.Model): # [v4 - added]
    observation_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="observation", on_delete=models.CASCADE)
    client_type_mc_ids = ArrayField(models.IntegerField(),default=list)
    has_difficulty_communicating = models.BooleanField(default=False)
    has_difficulty_understanding = models.BooleanField(default=False)
    has_difficulty_making_decision = models.BooleanField(default=False)
    need_help_cleaning = models.BooleanField(default=False)
    need_help_eating = models.BooleanField(default=False)
    need_help_toilet = models.BooleanField(default=False)
    need_help_hygiene = models.BooleanField(default=False)
    need_help_clothing = models.BooleanField(default=False)

    need_help_with_laundry = models.BooleanField(default=False)
    need_help_cooking = models.BooleanField(default=False)

    mobility_profile_mc_id = models.IntegerField(blank=True, null=True)
    mobility_equipment_mc_ids = ArrayField(models.IntegerField(),default=list)
    living_circumstances_mc_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_observation'


class SuSuspend(models.Model): # [v4 - added]
    su_suspend_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="su_suspend", on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    bcrs = JSONField(default=list)
    attachments = ArrayField(models.IntegerField(),default=list)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_suspend'


class SuScheduleOverrides(models.Model):
    schedule_override_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="su_schedule_override", on_delete=models.CASCADE)
    weekly_booking_id = models.IntegerField(blank=True, null=True)
    original_start_dt =  models.DateTimeField(blank=True, null=True)
    original_end_dt = models.DateTimeField(blank=True, null=True)
    overridden_start_dt = models.DateTimeField(blank=True, null=True)
    overridden_end_dt = models.DateTimeField(blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    schedule_override_type_mc_id = models.IntegerField(blank=True, null=True)
    schedule_override_status_mc_id = models.IntegerField(blank=True, null=True)
    admin_remark = models.CharField(max_length=200, blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_schedule_overrides'


class CarePlanPricingPlan(models.Model):
    cp_pricing_plan_id = models.AutoField(primary_key=True)
    funding_type_mc_id = models.IntegerField(blank=True, null=True)
    funding_sub_type_mc_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_stale = models.BooleanField(default=False)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_cp_pricing_plan'


class CarePlanPricingCode(models.Model):
    price_code_id = models.AutoField(primary_key=True)
    pricing_plan = models.ForeignKey('CarePlanPricingPlan', related_name="cp_pricing_plan", on_delete=models.CASCADE)
    weekday = models.FloatField(blank=True, null=True)
    saturday = models.FloatField(blank=True, null=True)
    sunday = models.FloatField(blank=True, null=True)
    bank_holiday = models.FloatField(blank=True, null=True)
    booking_type_mc_id = models.IntegerField(blank=True, null=True)
    duration_range_start = models.IntegerField(blank=True, null=True) #duration_gt
    duration_range_end = models.IntegerField(blank=True, null=True) #duration_lte
    is_fixed = models.BooleanField(blank=False, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_su_cp_pricing_code'