from django.db import models
from django.utils import timezone
from utils.models import Data
from math import floor

class StaffLeave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="staff_leave", on_delete=models.CASCADE)
    leave_type_mc_id = models.IntegerField(blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    leave_status_mc_id = models.IntegerField(blank=True, null=True) # 1: Approved, 2: Rejected, 3: Pending
    note = models.CharField(max_length=200, blank=True, null=True)
    admin_remark = models.CharField(max_length=200, blank=True, null=True) # [v2 - added]
    leave_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_staff_leave'


class StaffLeaveSummary(models.Model):
    leave_summary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="staff_leave_summary")
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

    annual_leave_accrued = models.FloatField(default=0)
    medical_leave_accrued = models.FloatField(default=0)
    days_per_week = models.IntegerField(blank=True, null=True, default=5)

    class Meta:
        managed = True
        db_table = 'hcms_staff_leave_summary'


class StaffBankDetail(models.Model):
    bank_detail_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="staff_bank_details", on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)
    sort_code = models.CharField(max_length=50, blank=True, null=True)
    account_type_mc_id = models.IntegerField(blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_staff_bank_detail'


class StaffRecruitment(models.Model):
    recruitment_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="staff_recruitment")
    application_date = models.DateTimeField(blank=True, null=True)
    source_text = models.CharField(max_length=100, blank=True, null=True)
    interview_date = models.DateTimeField(blank=True, null=True)
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
        db_table = 'hcms_staff_recruitment'



class StaffEmploymentRecord(models.Model):
    employment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="staff_employment_record", on_delete=models.CASCADE)
    employment_contract_type_mc_id = models.IntegerField(blank=True, null=True)
    employment_status = models.IntegerField(blank=True, null=True) # CURRENT, HISTORIC, TERMINATED
    no_of_entitled_holiday = models.SmallIntegerField(blank=True, null=True)
    availability_hr = models.IntegerField(blank=True, null=True)  # [v2 - added]
    signed_on = models.DateTimeField(blank=True, null=True)  # [v2 - added]
    start_date = models.DateTimeField(blank=True, null=True)  # [v2 - added]
    end_date = models.DateTimeField(blank=True, null=True)  # [v2 - added]
    terminated_on = models.DateTimeField(blank=True, null=True)  # [v2 - added]
    terminated_admin_remark = models.CharField(max_length=500, blank=True, null=True) # [v2 - added]
    contract_doc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    revised_origin = models.IntegerField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_staff_employment'

class StaffSuspendedRecord(models.Model):
    suspended_record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="staff_suspended_record")  # careworker
    started_date = models.DateTimeField(blank=True, null=True)
    finished_date = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    suspend_status_mc_id = models.IntegerField(blank=True, null=True) # added on 18 July

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_staff_suspended_record'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.User', related_name="staff", on_delete=models.CASCADE)
    visa_status_mc_id = models.IntegerField(blank=True, null=True) # [v2 - added]
    visa_expiry_date = models.DateTimeField(blank=True, null=True)
    passport_number = models.CharField(max_length=200, blank=True, null=True) # [v2 - added]
    passport_expiry_date = models.DateTimeField(blank=True, null=True) # [v2 - added]
    payroll_number = models.CharField(max_length=45, blank=True, null=True) # [v2 - added]
    nationality_mc_id = models.IntegerField(blank=True, null=True)
    staff_status_mc_id = models.IntegerField(blank=True, null=True)  # [v2 - added] active, suspended, leave, terminated
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
        db_table = 'hcms_staff_staff'


