from django.db import models
from django.utils import timezone
from cw.models import Document, EmploymentRecord
from django.contrib.postgres.fields import JSONField


# Create your models here.
class CWCost(models.Model):
    cost_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('ScheduledBooking', on_delete=models.CASCADE)
    care_worker_id = models.IntegerField(blank=True, null=True)
    is_override_amount = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    payslip = models.IntegerField(blank=True, null=True)
    is_override_taken_leave = models.BooleanField(default=False)
    taken_leave_mins = models.SmallIntegerField(blank=True, null=True)
    agency_invoice = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_cw_cost'


class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('ScheduledBooking', on_delete=models.CASCADE)
    expense_mc_id = models.IntegerField(blank=True, null=True)
    units = models.IntegerField(blank=True, null=True)
    charge = models.IntegerField(blank=True, null=True)
    pay = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_expense'



from su import models as su_model
from cw import models as cw_model
from django.db.models import F,Sum
class EngineRun(models.Model):
    engine_run_id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    engine_run_status_mc_id = models.IntegerField(blank=True, null=True)

    is_notified = models.BooleanField(default=False)

    booking_count = models.IntegerField(blank=True, null=True)
    allocated_count = models.IntegerField(blank=True, null=True)

    allocation_preset_mc_id = models.IntegerField(blank=True, null=True) #CENTRIC_MODE: Care Worker Centric,Service User Centric,Management Centric
    su_weight = models.IntegerField(blank=True, null=True)
    cw_weight = models.IntegerField(blank=True, null=True)
    mgt_weight = models.IntegerField(blank=True, null=True)
    allow_hard_violation = models.BooleanField(default=False)  #True: consider hard failed ones
    max_travel_time = models.IntegerField(blank=True, null=True)
    travel_time_enforcement = models.IntegerField(blank=True, null=True)
    change_percentage = models.FloatField(blank=True, null=True)
    inequality_skew = models.IntegerField(blank=True, null=True)
    critical_booking_priority = models.FloatField(blank=True, null=True)
    private_booking_priority = models.FloatField(blank=True, null=True)

    # engine_run_type_mc_id = models.IntegerField(blank=True, null=True)  #ENGINE_RUN_TYPE:  Full: (allocated+unallocated) , Partial: (unallocated only)
    reallocate_existing_bookings = models.BooleanField(default=False)  #True: full run

    is_stale = models.BooleanField(default=False)

    error = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    ended_date = models.DateTimeField(blank=True, null=True)

    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    changed_count = models.IntegerField(blank=True, null=True)
    high_quality_count = models.IntegerField(blank=True, null=True)
    medium_quality_count = models.IntegerField(blank=True, null=True)
    low_quality_count = models.IntegerField(blank=True, null=True)
    unallocated_count = models.IntegerField(blank=True, null=True)
    avg_quality = models.FloatField(blank=True, null=True)
    avg_quality_critical = models.FloatField(blank=True, null=True)
    avg_quality_private = models.FloatField(blank=True, null=True)
    avg_quality_other = models.FloatField(blank=True, null=True)
    su_satisfaction = models.FloatField(blank=True, null=True)
    cw_satisfaction = models.FloatField(blank=True, null=True)
    mgt_satisfaction = models.FloatField(blank=True, null=True)
    travel_time_exeed_count = models.IntegerField(blank=True, null=True)
    hard_failure_count = models.IntegerField(blank=True, null=True)
    raw_report = models.ForeignKey(Document, related_name="raw_doc", on_delete=models.CASCADE, null=True, default=None)
    notified_report = models.ForeignKey(Document, related_name="notified_doc", on_delete=models.CASCADE, null=True, default=None)
    is_terminated = models.BooleanField(default=False)
    engine_booking_stats = JSONField(blank=True, null=True)
    schedule_report = models.ForeignKey(Document, related_name="schedule_report_doc", on_delete=models.CASCADE, null=True,
                                        default=None)

    class Meta:
        managed = True
        db_table = 'hcms_bm_engine_run'



from django.db.models import Q
from background_task import background
from django.contrib.postgres.fields import ArrayField
import datetime
class ScheduledBooking(models.Model):
    scheduled_booking_id = models.AutoField(primary_key=True)
    service_user = models.ForeignKey('users.User', related_name="scheduled_booking", on_delete=models.CASCADE) # for whom
    weekly_booking_id = models.IntegerField(blank=True, null=True)
    # booking_quality = models.ForeignKey(BookingQuality, on_delete=models.CASCADE)
    started_date_time = models.DateTimeField(blank=True, null=True)
    finished_date_time = models.DateTimeField(blank=True, null=True)
    # cw1 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='care_worker_1')
    # cw2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='care_worker_2')
    no_of_cw = models.SmallIntegerField(blank=True, null=True)
    booking_type_mc_id = models.IntegerField(blank=True, null=True)
    booking_code = models.CharField(max_length=10,blank=True, null=True) #randomvalue
    booking_allocation_result_mc_id = models.IntegerField(blank=True, null=True)  # BOOKING_ALLOCATION_RESULT Pending,No Match,Allocated, Partially Allocated # [v2 - added]
    booking_status_mc_id = models.IntegerField(blank=True, null=True)  # BOOKING_STATUS: New,Past,Temp, Canceled, Rescheduled # [v2 - added]
    funding_type_mc_id = models.IntegerField(blank=True, null=True)  # FUNDING_TYPE: Local Authority, Self Funded
    funding_sub_type_mc_id = models.IntegerField(blank=True, null=True)  # FUNDING_SUB_TYPE: Local Authority, Self Funded
    is_critical = models.BooleanField(default=False)
    care_plan_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    common_cws = ArrayField(models.IntegerField(),default=list, blank=True, null=True)

    engine_run_id = models.IntegerField(blank=True, null=True)
    is_notified = models.BooleanField(default=False)

    is_unresolved = models.BooleanField(default=False)

    exceptions = models.TextField(blank=True, null=True) #excempted cws. list of strings

    certificate_expiry_id =  models.IntegerField(blank=True, null=True)
    cw_termination_id =  models.IntegerField(blank=True, null=True)
    cw_suspension_id = models.IntegerField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_scheduled_booking'



class BookingAllocation(models.Model):
    booking_allocation_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('ScheduledBooking', related_name="booking_allocation", on_delete=models.CASCADE)
    sequence = models.SmallIntegerField(blank=True, null=True)
    careworker = models.IntegerField(blank=True, null=True) # default - NULL #todo add foriegn key

    booking_quality = models.FloatField(blank=True, null=True) # default - NULL
    travel_time = models.IntegerField(default=True, null=True) # default - NULL
    is_changed = models.BooleanField(default=False)

    allocation_type_mc_id = models.IntegerField(blank=True, null=True)  # NULL, Lock, Auto, Override, Manual # default - NULL

    #[V3 -added]
    service_start_date_time = models.DateTimeField(blank=True, null=True)
    service_start_report_method_mc_id = models.IntegerField(blank=True, null=True)  #SERVICE_START_REPORT_METHOD, System, Manual
    service_start_status_mc_id = models.IntegerField(blank=True, null=True)  #SERVICE_START_STATUS : Pending,Late,Attended, No Show

    service_end_date_time = models.DateTimeField(blank=True, null=True)
    service_end_report_method_mc_id = models.IntegerField(blank=True, null=True)  #SERVICE_END_REPORT_METHOD, System, Manual
    service_end_status_mc_id = models.IntegerField(blank=True, null=True)  #SERVICE_END_STATUS : Pending, Interrupted, Left
    #[V3 -added end]

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_allocation'



from django.contrib.postgres.fields import JSONField,ArrayField
class BookingAllocationQuality(models.Model):
    allocation_quality_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('ScheduledBooking', related_name="booking_allocation_quality_booking", on_delete=models.CASCADE)
    careworker = models.ForeignKey('users.User', related_name="booking_allocation_quality_careworker", on_delete=models.CASCADE)
    is_hard_failed = models.BooleanField(default=False)
    is_cw_hard_failed = models.BooleanField(default=False)
    is_su_hard_failed = models.BooleanField(default=False)
    service_centric_score = models.FloatField(blank=True, null=True)
    profit_centric_score = models.FloatField(blank=True, null=True)
    cw_centric_score = models.FloatField(blank=True, null=True)
    overall_quality = models.FloatField(blank=True, null=True)
    availability_adjusted = models.BooleanField(default=False)

    is_travel_time_exceeds = models.BooleanField(default=False)
    travel_time = models.IntegerField(blank=True, null=True)
    travel_time2 = models.IntegerField(blank=True, null=True)
    incompatible_comment = ArrayField(models.IntegerField(),default=list)
    su_match = JSONField(blank=True, null=True)
    cw_match = JSONField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_allocation_quality'
        unique_together = ("booking", "careworker")

class SUCharge(models.Model):
    charge_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(ScheduledBooking, on_delete=models.CASCADE)
    service_user_id = models.IntegerField(blank=True, null=True)
    is_override_amount = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    is_external_invoiced = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_su_charge'


class SUFunding(models.Model):
    funding_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('ScheduledBooking', on_delete=models.CASCADE)
    service_user_id = models.IntegerField(blank=True, null=True)
    funder_id = models.IntegerField(blank=True, null=True)
    invoice_number = models.IntegerField(blank=True, null=True)
    amount = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_su_funding'


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(ScheduledBooking, related_name="booking_tasks", on_delete=models.CASCADE)
    template = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    is_completed =  models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_task'

from django.contrib.postgres.fields import ArrayField
class TaskTemplate(models.Model):
    task_template_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    booking_type = models.ForeignKey("utils.HcmsUtilsMasterCode",blank=True, null=True,on_delete=models.CASCADE,limit_choices_to={'code_type': "BOOKING_TYPE"})
    is_default =  models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        unique_together = ('title', 'booking_type')
        db_table = 'hcms_bm_task_template'

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class BookingChangeRequest(models.Model): # [v2 - added]
    booking_change_request_id = models.AutoField(primary_key=True)
    prev_booking = models.ForeignKey('ScheduledBooking', related_name="change_booking_prev", on_delete=models.CASCADE,blank=True, null=True)
    new_booking = models.ForeignKey('ScheduledBooking', related_name="change_booking_new", on_delete=models.CASCADE,blank=True, null=True)
    new_wb_id = models.IntegerField(blank=True, null=True)
    booking_change_request_type_mc_id = models.IntegerField(blank=True, null=True) # BOOKING_CHANGE_REQUEST_TYPE - ['Cancel', 'Reschedule']
    booking_change_request_status_mc_id = models.IntegerField(blank=True, null=True)  # BOOKING_CHANGE_REQUEST_STATUS - ['Pending', 'Approved', 'Rejected', 'Expired']

    admin_remark = models.CharField(max_length=200, blank=True, null=True)
    reason_object_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='bcr_reason', on_delete=models.CASCADE)
    reason_object_id = models.CharField(max_length=255, blank=True, null=True)
    reason_object = GenericForeignKey('reason_object_content_type', 'reason_object_id')

    missed_booking = models.ForeignKey('ScheduledBooking', related_name="change_booking_missed", on_delete=models.CASCADE,blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_booking_change_request'


    @property
    def service_user(self):
        if self.prev_booking:
            return self.prev_booking.service_user
        elif self.new_booking:
            return self.new_booking.service_user


from django.contrib.postgres.fields import JSONField
class BookingGen(models.Model):
    booking_gen_id = models.AutoField(primary_key=True)
    start_date_time = models.DateTimeField()
    finish_date_time = models.DateTimeField()
    log = JSONField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_bm_booking_gen'
        verbose_name = "Booking Generation"

import operator
from django.db.models import Count
class BookingHistory(models.Model):
    booking_history_id = models.AutoField(primary_key=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    log = JSONField(blank=True, null=True)
    past_month_record = None

    class Meta:
        managed = True
        db_table = 'hcms_bm_booking_history'

