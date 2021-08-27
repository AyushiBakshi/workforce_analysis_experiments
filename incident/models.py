from django.db import models
from django.utils import timezone

# Create your models here.
class IncidentReport(models.Model):
    incident_report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="incident_report", on_delete=models.CASCADE)
    is_urgent = models.BooleanField(default=False)  # 0: not urgent(default), 1: urgent
    reporter_role_id = models.SmallIntegerField(blank=True, null=True)
    reporter_staff = models.IntegerField(blank=True, null=True)  # by which user
    reporter_non_staff = models.CharField(max_length=150, blank=True, null=True)
    reporter_phone = models.CharField(max_length=45, blank=True, null=True)
    for_user = models.IntegerField(blank=True, null=True) # incident report for this user
    reporter_note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    # admin part
    is_resolved = models.BooleanField(default=False)  # 0: unresolved(default), 1: resolved
    admin_remark = models.TextField(blank=True, null=True) # by coordinator
    action_items_done = models.CharField(max_length=200, blank=True, null=True) # mc_id(s) only, "1, 2, 3, ...""
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_incident_report'


class Incident(models.Model):
    incident_id = models.AutoField(primary_key=True)
    about_user = models.ForeignKey('users.User', related_name="incident", on_delete=models.CASCADE) # User ID of User the incident is about
    reported_by_user = models.IntegerField(blank=True, null=True)
    reported_by_unregistered_user = models.CharField(max_length=150, blank=True, null=True)
    reported_date = models.DateTimeField(blank=True, null=True)
    incident_date = models.DateTimeField(blank=True, null=True)
    incident_location = models.CharField(max_length=200, blank=True, null=True)
    incident_details = models.TextField(blank=True, null=True)
    witness_user = models.IntegerField(blank=True, null=True)
    witness_details = models.TextField(blank=True, null=True)
    is_treatment_provided = models.BooleanField(default=False)
    is_injury_occurred = models.BooleanField(default=False)
    injury_description = models.TextField(blank=True, null=True)
    related_booking_id = models.IntegerField(blank=True, null=True)
    # admin part
    incident_status_mc_id = models.IntegerField(blank=True, null=True)
    admin_remark = models.TextField(blank=True, null=True)  # by coordinator
    ###
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True) # who created this record
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_incident'
