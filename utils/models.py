from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
import datetime, uuid

# Create your models here.
class HcmsUtilsMasterCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    code_type = models.CharField(max_length=100, blank=True, null=True)
    code_sub_type = models.CharField(max_length=100, blank=True, null=True)
    code_no = models.CharField(max_length=45, blank=True, null=True)
    code_val = models.CharField(max_length=150, blank=True, null=True)
    code_description = models.CharField(max_length=200, blank=True, null=True)
    display_label = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_utils_master_code'

    def add_config(code_type,code_val,created_by):
        HcmsUtilsMasterCode.objects.get_or_create(
            code_type  = code_type,
            code_val  = code_val,
            created_by  = created_by,
            last_modified_by  = created_by ,
            delete_ind  = 'N'
        )

    def __str__(self):
       return self.code_val

from django.contrib.postgres.fields import JSONField
class HCMSConfig(models.Model):
    VISIBILITY_LEVELS = (
            ('0', 'Hidden'),
            ('1', 'One Time'),
            ('2', 'All'),
        )
    code_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    code_type = models.CharField(max_length=100, blank=True, null=True)
    code_sub_type = models.CharField(max_length=100, blank=True, null=True)
    code_no = models.IntegerField(blank=True, null=True)
    code_val = models.CharField(max_length=150, blank=True, null=True)
    code_description = models.CharField(max_length=200, blank=True, null=True)
    code_name = models.CharField(max_length=200, blank=True, null=True)
    visibility_level = models.CharField(max_length=1, choices=VISIBILITY_LEVELS, default='0')
    validation = JSONField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_utils_config'

    def description(self):
        return mark_safe(self.code_description)


class ProviderConfig(HCMSConfig):
    class Meta:
        proxy = True

class LeaveSummaryConfig(HCMSConfig):
    class Meta:
        proxy = True
        verbose_name = 'CW Leave Entitlement Config'
        verbose_name_plural = 'CW Leave Entitlement Configs'

class EngineConfig(HCMSConfig):
    class Meta:
        proxy = True

class GeneralConfig(HCMSConfig):
    class Meta:
        proxy = True

class WeightsConfig(HCMSConfig):
    class Meta:
        proxy = True

class TravelTimeConfig(HCMSConfig):
    class Meta:
        proxy = True


class MedicationPrescriptionConfig(HCMSConfig):
    class Meta:
        proxy = True


class Data:
    MASTER_CODES = {}

    def init_mc_cache():
        full_data = HcmsUtilsMasterCode.objects.filter().values('code_type','code_val','code_id')
        master_codes = {}
        for data in full_data:
            if data['code_type'] in master_codes.keys():
                master_codes[data['code_type']].update({data['code_val']:data['code_id']})
            else:
                master_codes[data['code_type']] = {data['code_val']:data['code_id']}
        return master_codes
        
    def record(code_id):
        return HcmsUtilsMasterCode.objects.filter(code_id=code_id).values(
            'code_type','code_no','code_val','code_description')[0]
    
    def by_type(type_name):
        return list(HcmsUtilsMasterCode.objects.filter(code_type=type_name).values(
            'code_id','code_no','code_val','code_description'))

    def value(code_id):
        return HcmsUtilsMasterCode.objects.filter(code_id=code_id).values('code_val')[0]['code_val']

    def display_label(code_id):
        code_obj = HcmsUtilsMasterCode.objects.filter(code_id=code_id).first()
        if code_obj.display_label:
            return code_obj.display_label
        else:
            return code_obj.code_val

    def desc(code_id):
        return HcmsUtilsMasterCode.objects.filter(code_id=code_id).values('code_description')[0]['code_description']

    def desc_s(code_id):
        return HcmsUtilsMasterCode.objects.filter(code_id=code_id).values('code_description')[0]['code_description'].split(",")

    def code(code_type,code_val):
        if not Data.MASTER_CODES:
            Data.MASTER_CODES = Data.init_mc_cache()
        try:
            return Data.MASTER_CODES[code_type][code_val]    
        except Exception as e:
            Data.MASTER_CODES[code_type][code_val] = HcmsUtilsMasterCode.objects.filter(code_type=code_type,code_val=code_val).values('code_id')[0]['code_id']
            return Data.MASTER_CODES[code_type][code_val]    
    
    def c_code(code_type,code_val):
        return HCMSConfig.objects.filter(code_type=code_type,code_val=code_val).values('code_id')[0]['code_id']

    def c_value(type_name,sub_type=None):
        if sub_type:
            return HCMSConfig.objects.get(code_type = type_name, code_sub_type = sub_type).code_val
        else:
            return HCMSConfig.objects.get(code_type = type_name).code_val

    def c_by_type(type_name):
        tuple_list = HCMSConfig.objects.filter(code_type = type_name).values_list("code_sub_type","code_val")
        return {record[0]:(int(record[1])) for record in tuple_list}

    def start_license_expiration(requester_id):
        exp = HCMSConfig.objects.get(code_type = "LICENSE_PARAMS", code_sub_type = "Expiration")
        days = HCMSConfig.objects.get(code_type = "LICENSE_PARAMS", code_sub_type = "Grace Period").code_val
        if not exp.code_val:
            exp_date = (timezone.now()+datetime.timedelta(days=int(days))).replace(tzinfo=None)
            exp.code_val = str(exp_date)
            exp.last_modified_by = requester_id
            exp.last_modified_date = timezone.now()
            exp.save()

    def is_license_violated_due_to_user_list_change(engine_id):
        from booking.models import EngineRun, BookingAllocation

        last_notified_engine_run = EngineRun.objects.filter(delete_ind='N',
                                                            engine_run_status_mc_id=Data.code("ENGINE_RUN_STATUS",
                                                                                              "Approved")).order_by(
            '-finish_date').first()
        curr_engine_run = EngineRun.objects.filter(pk=engine_id).first()
        if last_notified_engine_run and curr_engine_run:
            last_notified_week_end = last_notified_engine_run.finish_date
            last_notified_week_start = (last_notified_week_end - datetime.timedelta(days=7)).replace(hour=0, minute=0,
                                                                                                     second=0,
                                                                                                     microsecond=0)

            last_notified_bookings = BookingAllocation.objects.filter(
                booking__started_date_time__range=(last_notified_week_start, last_notified_week_end),
                booking__is_notified=True)

            last_notified_cw_list = set(last_notified_bookings.values_list('careworker', flat=True))
            last_notified_su_list = set(last_notified_bookings.values_list('booking__service_user', flat=True))

            current_engine_run_bookings = BookingAllocation.objects.filter(
                booking__started_date_time__range=(curr_engine_run.start_date, curr_engine_run.finish_date))

            current_cw_list = set(current_engine_run_bookings.values_list('careworker', flat=True))
            current_su_list = set(current_engine_run_bookings.values_list('booking__service_user', flat=True))

            cw_list_diff_ratio = int(len((last_notified_cw_list - current_cw_list)) / len(last_notified_cw_list) if last_notified_cw_list else 0)
            su_list_diff_ratio = int(len((last_notified_su_list - current_su_list)) / len(last_notified_su_list) if last_notified_su_list else 0)

            CW_CHANGE_PERCENT_THRESHOLD = int(Data.c_value('LICENSE_PARAMS', 'CW Change Threshold Percent'))
            SU_CHANGE_PERCENT_THRESHOLD = int(Data.c_value('LICENSE_PARAMS', 'SU Change Threshold Percent'))
            if cw_list_diff_ratio * 100 > CW_CHANGE_PERCENT_THRESHOLD:
                return True

            if su_list_diff_ratio * 100 > SU_CHANGE_PERCENT_THRESHOLD:
                return True

        return False

    def is_license_expired(date):
        exp = HCMSConfig.objects.get(code_type = "LICENSE_PARAMS", code_sub_type = "Expiration").code_val
        if exp: 
            exp_date = datetime.datetime.strptime(exp, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)
            return exp_date <= timezone.now() or exp_date <= date
        else:
            return False


class TravelTimeRelatedProcessesHistory(models.Model):
    id = models.AutoField(primary_key=True)
    coordinates = models.TextField(blank=True, null=True)
    tt_process = models.TextField(blank=True, null=True)
    map_status = models.TextField(default="INITIALIZED")
    map_error = models.TextField(blank=True, null=True)
    engine_run_status = models.TextField(blank=True, null=True)
    engine_run_progress = models.TextField(blank=True, null=True)
    engine_run_error = models.TextField(blank=True, null=True)
    engine_progress_last_modified_date = models.DateTimeField(blank=True, null=True)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')
    completed_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hcms_ttg_processes_history'



class TravelTimeCoordinateSaveHistory(models.Model):
    id = models.AutoField(primary_key=True)
    old_coordinates = models.TextField(blank=True, null=True)
    new_coordinates = models.TextField(blank=False, null=False)
    is_current = models.BooleanField(null=True)
    excluded_users_status = models.TextField(blank=True, null=True)
    excluded_cw = ArrayField(models.CharField(max_length=150, blank=True, null=True), default=list)
    excluded_su = ArrayField(models.CharField(max_length=150, blank=True, null=True), default=list)
    excluded_users_error = models.TextField(blank=True, null=True)
    related_tt_process = models.ForeignKey(TravelTimeRelatedProcessesHistory, on_delete=models.CASCADE, blank=True, null=True)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')
    completed_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hcms_ttg_coordinate_history'


class TravelTimeRelatedProcesses(models.Model):
    process_id = models.AutoField(primary_key=True)
    process_name = models.TextField(blank=True, null=True)
    process_no =models.IntegerField(blank=True, null=True)
    process_description = models.TextField(blank=True, null=True)
    process_action = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_ttg_processes'

    def description(self):
        return mark_safe(self.process_description)

    def remark(self):
         return mark_safe(self.remarks)


class GenerateTravelTimeStandardMode(TravelTimeRelatedProcesses):
    class Meta:
        proxy = True
        verbose_name = 'Generate travel time'
        verbose_name_plural = 'Generate travel time'


class GenerateTravelTimeAdvancedMode(TravelTimeRelatedProcesses):
    class Meta:
        proxy = True
        verbose_name = 'Update travel time'
        verbose_name_plural = 'Update travel time'

class ReportExportHistory(models.Model):
    report_export_id = models.AutoField(primary_key=True)
    report_type = models.IntegerField(blank=True, null=True)
    report_format = models.CharField(max_length=150, blank=True, null=True)
    report_contents = ArrayField(models.CharField(max_length=150, blank=True, null=True),default=list)
    report_start_dt = models.DateTimeField()
    report_end_dt = models.DateTimeField()
    report_generated_for = ArrayField(models.IntegerField(),default=list)
    exported_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_report_export_history'

class DataLock(models.Model):
    data_lock_id = models.AutoField(primary_key=True)
    object_id = models.IntegerField(blank=True, null=True)
    object_type = models.CharField(max_length=150,blank=True, null=True)
    locked_by_user_name = models.CharField(max_length=50,blank=True, null=True)
    user_name =  models.CharField(max_length=50,blank=True, null=True)
    last_modified_on = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'hcms_utils_data_lock'


class FilterPreset(models.Model):
    preset_id = models.AutoField(primary_key=True)
    preset_type = models.CharField(max_length=150,blank=True, null=True)
    preset_name = models.CharField(max_length=150,blank=True, null=True)
    preset_category = models.CharField(max_length=50,blank=True, null=True)
    preset_value = JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hcms_utils_filter_preset'


class EmailProof(models.Model):
    email_proof_id = models.AutoField(primary_key=True)
    email_proof_token = models.UUIDField(default=uuid.uuid4)
    email = models.CharField(max_length=255, blank=True, null=True)
    email_proof_purpose_mc_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'hcms_utils_email_proof'
