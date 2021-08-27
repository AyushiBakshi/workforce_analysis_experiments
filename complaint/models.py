from django.db import models
from django.utils import timezone

# Create your models here.
class ComplaintCompliment(models.Model):
    complaint_compliment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="complaint_compliment", on_delete=models.CASCADE) # reporter
    is_complaint = models.BooleanField(default=False) # 0: compliment(default), 1: complaint
    is_urgent = models.BooleanField(default=False)  # 0: not urgent(default), 1: urgent
    category_mc_id = models.IntegerField(blank=True, null=True)
    # critical_level_mc_id = models.IntegerField(blank=True, null=True) # Ignore, Low, Medium, High
    for_user = models.IntegerField(blank=True, null=True) # for this user
    reported_user_role_id = models.SmallIntegerField(blank=True, null=True)
    reported_user = models.IntegerField(blank=True, null=True) # by which user
    reporter_note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now) # report_created_date
    created_by = models.IntegerField(blank=True, null=True) # report_created_by
    # admin part
    is_resolved = models.BooleanField(default=False)  # 0: unresolved(default), 1: resolved
    scoring_level = models.SmallIntegerField(blank=True, null=True)
    scoring_remark = models.TextField(blank=True, null=True)
    admin_remark = models.TextField(blank=True, null=True) # by coordinator or manager
    action_items_done = models.CharField(max_length=200, blank=True, null=True) # mc_id(s) only, "1, 2, 3, ...""
    last_modified_date = models.DateTimeField(default=timezone.now) # report_managed_date
    last_modified_by = models.IntegerField(blank=True, null=True) # report_managed_by
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_complaint_compliment'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey('users.User', related_name="feedback_from", on_delete=models.CASCADE) # reporter
    about_user = models.ForeignKey('users.User', related_name="feedback_about", on_delete=models.CASCADE, blank=True, null=True) # reportee
    feedback_nature_mc_id = models.IntegerField(blank=True, null=True) #FEEDBACK_NATURE: Complaint, Compliment
    feedback_topic_mc_id = models.IntegerField(blank=True, null=True) #FEEDBACK_TOPIC:Service Quality,Hygiene,Punctuality,Behavior, Others
    priority_mc_id = models.IntegerField(blank=True, null=True) #FEEDBACK_PRIORITY_LEVEL  Low, Medium, High
    related_booking_id = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    
    # admin part
    feedback_status_mc_id = models.IntegerField(blank=True, null=True) #FEEDBACK_STATUS  Pending, Ignored, Resolved
    feedback_score_level = models.SmallIntegerField(blank=True, null=True)
    feedback_score_remark = models.TextField(blank=True, null=True)
    admin_remark = models.TextField(blank=True, null=True) # by coordinator or manager
    action_items = models.CharField(max_length=200, blank=True, null=True) # mc_id(s) only, "1, 2, 3, ...""
    
    created_date = models.DateTimeField(default=timezone.now) # system user
    created_by = models.IntegerField(blank=True, null=True) # report_created_by
    last_modified_date = models.DateTimeField(default=timezone.now) # report_managed_date
    last_modified_by = models.IntegerField(blank=True, null=True) # report_managed_by
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_complaint_feedback'