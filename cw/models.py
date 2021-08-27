from django.db import models
from django.utils import timezone
import datetime
import os
import six, base64
import uuid
from math import floor

from channel.sync import notify_to_sync
from users.models import (
   User
)
from utils.models import Data
from django.contrib.postgres.fields import JSONField
from django.db.models import Q,Sum

# Create your models here.

class CareWorker(models.Model):
    care_worker_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="careworker", on_delete=models.CASCADE)
    carer_comment = models.CharField(max_length=200, blank=True, null=True)
    personal_number = models.CharField(max_length=45, blank=True, null=True)
    working_time_opt_out = models.IntegerField(blank=True, null=True)
    cw_left_reason_mc_id = models.IntegerField(blank=True, null=True)
    team = models.CharField(max_length=100, blank=True, null=True)  # id(s) only, "1, 2, 3, ...""
    visa_status_mc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    visa_expiry_date = models.DateTimeField(blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True) # [v2 - added]
    passport_expiry_date = models.DateTimeField(blank=True, null=True) # [v2 - added]
    payroll_number = models.CharField(max_length=20, blank=True, null=True) # [v2 - added]
    qualification = models.CharField(max_length=200, blank=True, null=True)
    nationality_mc_id = models.IntegerField(blank=True, null=True)
    transport_type_mc_id = models.IntegerField(blank=True, null=True)
    cw_status_mc_id = models.IntegerField(blank=True, null=True)  # [v2 - added] active, suspended, leave, terminated
    is_started_to_work = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    seniority_mc_id = models.IntegerField(blank=True, null=True)
    signed_off_by = models.IntegerField(blank=True, null=True)
    signed_off_date = models.DateTimeField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    passport_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    visa_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    residency_proof_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    is_permanent_uk_resident = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_care_worker'


class AvailabilityChangeRequest(models.Model):
    avail_request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="avail_cr", on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    started_time = models.TimeField(blank=True, null=True)
    finished_time = models.TimeField(blank=True, null=True)
    request_type_mc_id = models.IntegerField(blank=True, null=True) # sick leave, reschedule time, extra time etc
    request_comment = models.CharField(max_length=200, blank=True, null=True)
    status_mc_id = models.IntegerField(blank=True, null=True) # pending, approved or rejected
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_availability_change_request'

class CareWorkerStats(models.Model):
    cw_stat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="cw_stat_cw_id", on_delete=models.CASCADE)
    engine_run_id = models.IntegerField(blank=True, null=True)
    travel_time = models.FloatField(default = 0)
    contract_hours = models.FloatField(default = 0)
    allocated_hours = models.FloatField(default = 0)
    booking_count = models.IntegerField(default = 0)
    utilization_rate =  models.FloatField(default = 0)
    service_centric_score = models.FloatField(default = 0)
    profit_centric_score = models.FloatField(default = 0)
    cw_centric_score = models.FloatField(default = 0)
    overall_quality = models.FloatField(default = 0)
    class Meta:
        managed = True
        db_table = 'hcms_cw_cw_stats'



class BankDetail(models.Model):
    bank_detail_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="bank_details", on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    branch_name = models.CharField(max_length=200, blank=True, null=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)
    sort_code = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    account_type_mc_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_bank_detail'


class Awards(models.Model):
    award_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    award_mc_id = models.IntegerField(blank=True, null=True)
    month_mc_id = models.IntegerField(blank=True, null=True)
    amount_mc_id = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_carer_award'


class DBSDetail(models.Model):
    dbs_detail_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    entry_level_mc_id = models.IntegerField(blank=True, null=True)
    payment_type_mc_id = models.IntegerField(blank=True, null=True)
    result_mc_id = models.IntegerField(blank=True, null=True)
    is_received = models.BooleanField(default=False)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    applied_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_dbs_detail'


class EmploymentRecord(models.Model):
    employment_id = models.AutoField(primary_key=True)
    # user = models.OneToOneField('users.User', related_name="employment_record", on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name="employment_record", on_delete=models.CASCADE)
    employment_contract_type_mc_id = models.IntegerField(blank=True, null=True)
    team_mc_id = models.IntegerField(blank=True, null=True)
    care_worker_grade_mc_id = models.IntegerField(blank=True, null=True)
    work_through_agency = models.IntegerField(blank=True, null=True)
    contract_hours = models.FloatField(blank=True, null=True)
    pay_rate = models.FloatField(blank=True, null=True)
    pay_frequency_mc_id = models.IntegerField(blank=True, null=True)
    maximum_hours = models.TimeField(blank=True, null=True)
    employment_status = models.IntegerField(blank=True, null=True) # CURRENT, HISTORIC, TERMINATED
    badge_id = models.CharField(max_length=20, blank=True, null=True)
    has_uniform = models.BooleanField(default=False)
    signed_on = models.DateTimeField(blank=True, null=True)  # [v2 - added]
    start_date = models.DateTimeField()  # [v2 - added]
    end_date = models.DateTimeField()  # [v2 - added]

    revised_origin = models.IntegerField(blank=True, null=True)

    terminated_on = models.DateTimeField(blank=True, null=True)  # [v2 - added]

    contract_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]

    # moved from cw
    availability_hr = models.IntegerField()  # [v2 - added]
    proposed_hr = models.IntegerField(blank=True, null=True)  # [v2 - added]
    proposed_reason = models.CharField(max_length=200, blank=True, null=True)  # [v2 - added]
    revised_hr = models.IntegerField(blank=True, null=True)  # [v2 - added]
    revised_admin_remark = models.CharField(max_length=200, blank=True, null=True)  # [v2 - added]
    changed_hr_status_mc_id = models.IntegerField(blank=True, null=True)  # [v2 - added] CHANGED_HR_STATUS Pending,Rejected,Approved
    change_avail_hr_doc_id = models.IntegerField(blank=True, null=True)  # [v2 - added]
    job_title = models.CharField(max_length=150, blank=True, null=True) # added
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_employment'


class TerminationRequest(models.Model):
    termination_request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name='terminate_user', on_delete=models.CASCADE)
    proposed_date = models.DateTimeField()
    employment_record = models.ForeignKey('cw.EmploymentRecord', related_name='contract_termination', on_delete=models.CASCADE)

    remark = models.TextField(blank=True, null=True)
    termination_request_status_mc_id = models.IntegerField(blank=True, null=True) #Pending, Accepted, Rejected
    attachment = models.IntegerField(blank=True, null=True)
    report_doc = models.IntegerField(blank=True, null=True)
    admin_remark = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_termination_request'


class ExitInterview(models.Model):
    exit_interview_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    last_working_date = models.DateTimeField(blank=True, null=True)
    exit_interview_date = models.DateTimeField(blank=True, null=True)
    conducted_by_mc_id = models.IntegerField(blank=True, null=True)
    is_process_p45 = models.BooleanField(default=False)
    send_p45_mc_id = models.IntegerField(blank=True, null=True)
    left_reason = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_exit_interview'


class Holiday(models.Model):
    holiday_id = models.AutoField(primary_key=True)
    leave = models.OneToOneField('cw.Leave', related_name="holiday", on_delete=models.CASCADE)
    financial_year_mc_id = models.IntegerField(blank=True, null=True)
    cut_off_period_mc_id = models.IntegerField(blank=True, null=True)
    no_of_days_applied = models.SmallIntegerField(blank=True, null=True)
    no_of_days_pay_prior = models.SmallIntegerField(blank=True, null=True)
    no_of_days_paid = models.SmallIntegerField(blank=True, null=True)
    no_of_days_left = models.SmallIntegerField(blank=True, null=True)
    no_of_days_unpaid = models.SmallIntegerField(blank=True, null=True)
    is_paid_holiday = models.BooleanField(default=False)
    work_covered_by = models.IntegerField(blank=True, null=True)
    note_to_account = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    approved_by_coordinator = models.IntegerField(blank=True, null=True)
    approved_by_manager = models.IntegerField(blank=True, null=True)
    approved_by_sr_manager = models.IntegerField(blank=True, null=True)
    account_update_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_holiday'


class HolidayDetail(models.Model):
    holiday_detail_id = models.AutoField(primary_key=True)
    holiday = models.ForeignKey(Holiday, related_name="holiday_detail", on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    type_mc_id = models.IntegerField(blank=True, null=True) # full or half(am) or half(pm)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_holiday_detail'


class HolidayEntitlement(models.Model): # to be removed
    holiday_entitlement_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="holiday_entitlement")
    financial_year_mc_id = models.IntegerField(blank=True, null=True)
    entitlement = models.FloatField(blank=True, null=True)
    days_taken = models.FloatField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_holiday_entitlement'


class Recruitment(models.Model):
    recruitment_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="recruitment")
    application_date = models.DateTimeField(blank=True, null=True)
    # source_mc_id = models.IntegerField(blank=True, null=True)
    source_text = models.CharField(max_length=100, blank=True, null=True)
    interview_date = models.DateTimeField(blank=True, null=True)
    # interview_date_2 = models.DateTimeField(blank=True, null=True) # [v2 - added]
    # interview_date_3 = models.DateTimeField(blank=True, null=True) # [v2 - added]
    interviewer_1_id = models.IntegerField(blank=True, null=True)
    interviewer_2_id = models.IntegerField(blank=True, null=True)
    decision_mc_id = models.IntegerField(blank=True, null=True)
    decision_date = models.DateTimeField(blank=True, null=True)
    previous_employment_mc_id = models.IntegerField(blank=True, null=True)
    recruitment_note = models.CharField(max_length=200, blank=True, null=True)
    interview_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    recruitment_source_mc_id = models.IntegerField(blank=True, null=True) # [v4 - added]
    cv_doc_id = models.IntegerField(blank=True, null=True)  # [v2 - added]
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_recruitment'



class RecruitmentDoc(models.Model):
    doc_id = models.AutoField(primary_key=True)
    recruitment = models.ForeignKey(Recruitment, on_delete=models.CASCADE)
    doc_type_mc_id = models.IntegerField(blank=True, null=True)
    reference_person_id = models.IntegerField(blank=True, null=True)
    reference_no = models.CharField(max_length=45, blank=True, null=True)
    requested_on = models.IntegerField(blank=True, null=True)
    requested_date = models.DateTimeField(blank=True, null=True)
    requested_by_id = models.IntegerField(blank=True, null=True)
    accepted_on = models.IntegerField(blank=True, null=True)
    accepted_date = models.DateTimeField(blank=True, null=True)
    accepted_by_id = models.IntegerField(blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    doc_comment = models.CharField(max_length=200, blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_recruitment_doc'


class SalaryDetail(models.Model):
    salary_detail_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User',related_name="salary_detail", on_delete=models.CASCADE)
    is_standard_rate = models.BooleanField(default=False)
    team_mc_id = models.IntegerField(blank=True, null=True)
    position_mc_id = models.IntegerField(blank=True, null=True)
    rate_grade_mc_id = models.IntegerField(blank=True, null=True)
    weekend_rate = models.FloatField(blank=True, null=True)
    effective_date_from = models.DateField(blank=True, null=True)
    effective_date_to = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    rate_type_mc_id = models.IntegerField(blank=True, null=True)
    service_type_mc_id = models.IntegerField(blank=True, null=True)
    service_user_hours = models.CharField(max_length=200, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    is_authorised = models.BooleanField(default=False)
    authorised_by = models.IntegerField(blank=True, null=True)
    authorised_date = models.DateTimeField(blank=True, null=True)
    raised_by = models.IntegerField(blank=True, null=True)
    raised_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_salary_detail'


class ScheduledAvailability(models.Model):
    scheduled_availability_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="availability")
    day_of_week = models.IntegerField(blank=True, null=True) # MON, TUE, WED ....
    started_time = models.TimeField(blank=True, null=True)
    finished_time = models.TimeField(blank=True, null=True)
    availability_status_mc_id = models.IntegerField(blank=True, null=True)  # 1: Available, 2: Unavailable, 3: Booked, 4: Leave, 5: Holiday
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_scheduled_availability'


class ChangeWeeklySchedule(models.Model):
    change_weekly_schedule_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="change_weekly_schedule")
    # this column is intended to use in tracking original record from Availability tbl.
    scheduled_availability_id = models.IntegerField(blank=True, null=True) # default NULL for 'extra hour' records
    day_of_week = models.IntegerField(blank=True, null=True) # MON, TUE, WED ....
    started_time = models.TimeField(blank=True, null=True)
    finished_time = models.TimeField(blank=True, null=True)
    status_mc_id = models.IntegerField(blank=True, null=True)  # 1: Available, 2: Unavailable, 3: Booked, 4: Leave, 5: Holiday
    result_mc_id = models.IntegerField(blank=True, null=True) # Pending(default), Approved, Rejected
    remark = models.CharField(max_length=200, blank=True, null=True) # some remarks for the case of rejecting request, for example
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_change_weekly_schedule'

from django.contrib.postgres.fields import ArrayField
class Certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="cw_skill")
    skills = ArrayField(models.IntegerField(),default=list)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(blank=True, null=True)
    attachment_id = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')
    original_end_date = models.DateTimeField(blank=True, null=True)
    handle_bookings_until = models.DateTimeField(blank=True, null=True)
    bookings_handled = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'hcms_cw_certificate'

class SkillTemplate(models.Model):
    skill_template_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=200)
    is_mandatory = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_skill_template'


def get_skills():
    skills = SkillTemplate.objects.filter(delete_ind = 'N')
    skill_list = []
    for skill in skills:
        skill_list.append((skill.skill_name, skill.skill_name))
    skill_tup = tuple(skill_list)
    return skill_tup

from django.contrib.postgres.fields import ArrayField
class TrainingTemplate(models.Model):
    training_template_id = models.AutoField(primary_key=True)
    training_type = models.CharField(max_length=200, blank=True, null=True)
    duration = models.FloatField(verbose_name="Duration(Days)", default=1) #in days
    validity = models.IntegerField(blank=True, null=True,verbose_name="Validity(Years)") # in years
    items_covered = ArrayField(models.CharField(max_length=2000, choices=get_skills(), blank=True, null=True))
    init_training = models.BooleanField(default=False, verbose_name = "Initialization Training")
    is_stale = models.BooleanField(default=False, verbose_name = "Mark As Obsolete")
    class Meta:
        managed = True
        db_table = 'hcms_cw_training_template'

class Training(models.Model):
    training_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="training")
    training_template_id = models.IntegerField(blank=True, null=True)
    outcome_mc_id = models.IntegerField(blank=True, null=True)
    training_centre = models.TextField(blank=True, null=True)
    complete_by_date = models.DateTimeField(default=timezone.now)
    training_status_mc_id = models.IntegerField(blank=True, null=True)
    request_note = models.CharField(max_length=200, blank=True, null=True)
    completion_note = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_training'

class TrainingSlot(models.Model):
    training_slot_id = models.AutoField(primary_key=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    arrival_time = models.TimeField(blank=True, null=True)
    training_slot_status_mc_id = models.IntegerField(blank=True, null=True, default=Data.code('TRAINING_SLOT_STATUS','Active'))
    training = models.ForeignKey('Training', related_name="cw_training", on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_training_slots'


class HcmsCwPreference(models.Model):
    cw_preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="cw_preference", on_delete=models.CASCADE) # careworker
    # unique_key = models.CharField(max_length=128, blank=True, null=True) #random number, unique
    preference_type_mc_id = models.IntegerField(blank=True, null=True)
    # preference_value_mc_id = models.IntegerField(blank=True, null=True)
    preference_value = models.CharField(max_length=200, blank=True, null=True) # id(s) only, "1, 2, 3, ..."" # [v2 - added]
    incorporation_type_mc_id = models.IntegerField(blank=True, null=True) # soft, hard, like, dislike etc
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_preference'


class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="leave", on_delete=models.CASCADE)
    leave_type_mc_id = models.IntegerField(blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    leave_status_mc_id = models.IntegerField(blank=True, null=True) # 1: Approved, 2: Rejected, 3: Pending
    note = models.CharField(max_length=1000, blank=True, null=True)
    admin_remark = models.CharField(max_length=200, blank=True, null=True) # [v2 - added]
    leave_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_leave'



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<user_id>/<filename>
    # return 'user_{0}/{1}'.format(instance.user.user_id, filename)
    # return '{0}/{1}'.format(instance.type, filename)
    filename, file_extension = os.path.splitext(filename)
    path = instance.type
    # key, message
    # format = encode(str(timezone.now), str(instance.user_id)).decode("utf-8")
    format = str(filename) + '_' + str(uuid.uuid4())
    return os.path.join(path, format + file_extension)


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="document", blank=True, null=True, on_delete=models.CASCADE)
    doc_type_mc_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=False, null=False)
    file_path = models.TextField(blank=False, null=False)
    note = models.CharField(max_length=200, blank=True, null=True)
    # key = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_document'


class CwAvailability(models.Model):
    cw_availability_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="cw_availability") #careworker
    availability_status_mc_id = models.IntegerField(blank=True, null=True)  #'CURRENT', 'PENDING', 'HISTORIC', 'REJECTED', 'APPROVED'
    effective_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    prev_availability = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_availability'


class AvailabilitySlot(models.Model):
    availability_slot_id = models.AutoField(primary_key=True)
    cw_availability = models.ForeignKey('CwAvailability', on_delete=models.CASCADE, related_name="availability_slot")
    day_of_week = models.IntegerField() # MON, TUE, WED ....
    started_time = models.TimeField()
    finished_time = models.TimeField()

    biweekly_mc_id = models.IntegerField() # Every Week, Odd Week, Even Week

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_availability_slot'


class SuspendedRecord(models.Model):
    suspended_record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="suspended_record")  # careworker
    started_date = models.DateTimeField(blank=True, null=True)
    finished_date = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    attachment = models.IntegerField(blank=True, null=True)
    report_doc = models.IntegerField(blank=True, null=True)
    admin_remark = models.TextField(blank=True, null=True)
    suspend_status_mc_id = models.IntegerField(blank=True, null=True) # added on 18 July
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_cw_suspended_record'



class LeaveSummary(models.Model):
    leave_summary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="leave_summary")
    is_current = models.BooleanField(default=True)
    financial_year = models.IntegerField(blank=True, null=True)

    annual_leave_entitlement = models.FloatField()
    medical_leave_entitlement = models.FloatField()

    medical_leave_days_taken = models.FloatField(default=0)
    annual_leave_days_taken = models.FloatField(default=0)
    urgent_leave_days_taken = models.FloatField(default=0)
    leave_of_absence_days_taken = models.FloatField(default=0)

    annual_leave_carry_forward = models.FloatField(default=0)
    medical_leave_carry_forward = models.FloatField(default=0)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')
    typical_working_hrs_per_day = models.FloatField(default=0)
    annual_leave_accrued = models.FloatField(default=0)
    medical_leave_accrued = models.FloatField(default=0)
    days_per_week = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hcms_cw_leave_summary'

