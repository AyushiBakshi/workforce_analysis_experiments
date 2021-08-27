from django.db import models
from django.utils import timezone
import operator
import operator

# Create your models here.
class Performance(models.Model):
    performance_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', related_name="performance", on_delete=models.CASCADE) # careworker
    
    external_feedback_score = models.FloatField(default = 5, null=True)
    internal_feedback_score = models.FloatField(default = 5, null=True)
    dependability_score = models.FloatField(default = 5, null=True)
    time_keeping_score = models.FloatField(default = 5, null=True)
    alert_response_score = models.FloatField(default = 5, null=True)
    experience_score = models.FloatField(default = 5, null=True)
    skill_score = models.FloatField(default = 5, null=True)
    performance_score = models.FloatField(default = 5, null=True)

    seq = models.IntegerField(default = 0, null=True)
    performance_status_mc_id = models.IntegerField(blank=True, null=True) #PERFORMANCE _STATUS; current,past
    
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_performance_performance'



class Criteria(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    criteria_type = models.CharField(max_length=100, blank=True, null=True)
    criteria_weight=models.FloatField(blank=True, null=True)

    criteria_sub_type = models.CharField(max_length=100, blank=True, null=True)
    sub_type_seq = models.SmallIntegerField(blank=True, null=True)
    sub_type_match = models.SmallIntegerField(blank=True, null=True)
    sub_type_level = models.SmallIntegerField(blank=True, null=True)
    
  
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    class Meta:
        managed = True
        db_table = 'hcms_performance_criteria'


    