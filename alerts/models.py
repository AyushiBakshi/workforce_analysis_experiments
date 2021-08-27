from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
from django.apps import apps
import json
import operator
from django.db.models import Q
from functools import reduce
from users.models import User
import re
import functools
import datetime
from utils.models import Data
import booking as booking_models 
from django.core.validators import MinValueValidator, MaxValueValidator
class Trigger(models.Model):
    trigger_id = models.AutoField(primary_key=True)
    seq = models.SmallIntegerField(blank=True, null=True)
    label=models.CharField(max_length=50, blank=True, null=True) #unique for each origin triger
    recipients = models.CharField(max_length=50, blank=True, null=True)  #comma seperated. can be group no or field name of user
    senders = models.CharField(max_length=50, blank=True, null=True) # type of user
    action_user = models.CharField(max_length=50, blank=True, null=True) # user
    threshold = models.FloatField(blank=True, null=True) #time after origin notification # todo: in minutes
    threshold_type=models.CharField(max_length=1, blank=True, null=True)
    notification_type_mc_id = models.SmallIntegerField(blank=True, null=True) #NOTIFICATION_TYPE : Alert, Notification, Reminder, Request,
    verb = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    keyword = models.CharField(max_length=50, blank=True, null=True)
    event_date_field=models.CharField(max_length=50, blank=True, null=True) # type of user
    level = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(1),MaxValueValidator(10)])
    seen_closure=models.BooleanField(blank=True, null=True) 
    email = models.BooleanField(blank=False, null=True) 
    closure_field = models.CharField(max_length=200, blank=True, null=True)
    closure_condition = models.CharField(max_length=5, blank=True, null=True)
    
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')
    offset_days = models.CharField(max_length=10, blank=True, null=True)
    is_different_reminder = models.BooleanField(blank=False,null=True, default=False)
    notification_purpose_mc_id = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hcms_alerts_trigger'
        verbose_name = 'Priority Level'

    def __str__(self):
        return self.label

    @property
    def next(self):
        return Trigger.objects.filter(label=self.label,seq=self.seq+1).first()

    def get_recipients(self,obj=None):
        #special case: to get allocated cws of enginerun
        if self.recipients == "engine_run_users":
            allocs = booking_models.models.BookingAllocation.objects.filter(
                booking__booking_status_mc_id = Data.code("BOOKING_STATUS","New"),
                booking__booking_allocation_result_mc_id = Data.code("BOOKING_ALLOCATION_RESULT","Allocated"),
                booking__started_date_time__gte = obj.start_date,
                booking__started_date_time__lt = obj.finish_date,
                booking__delete_ind = 'N'
            )
            cws = set()
            sus = set()
            for alloc in allocs:
                cws.add(alloc.careworker)
                sus.add(alloc.booking.service_user.user_id)

            if self.label == 'roster_notify_su':
                recipients = list(sus)
            else:
                recipients = list(cws)

            user_list = User.objects.filter(user_id__in = recipients)
            return [(u,0) for u in user_list]

        #special case: to get allocated cws
        if self.recipients == "allocated_cws":
            booking = getattr(obj,"prev_booking") if hasattr(obj, 'prev_booking') else obj 
            allocations = booking_models.models.BookingAllocation.objects.filter(booking = booking)
            user_list = User.objects.filter(user_id__in = [allocation.careworker for allocation in allocations])
            return [(u,0) for u in user_list]

        #special case: to get allocated cws for both bookings in bcr
        if self.recipients == "same_allocated_cws":
            prev_cws = set(obj.prev_booking.booking_allocation.filter().values_list("careworker",flat=True))
            new_cws = set(obj.new_booking.booking_allocation.filter().values_list("careworker",flat=True))
            same_cws = list(prev_cws.intersection(new_cws))
            user_list = User.objects.filter(user_id__in = same_cws)
            return [(u,0) for u in user_list]

        if self.recipients == "booking_related_cws":
            users = list(booking_models.models.BookingAllocation.objects.filter(booking=obj).values_list('careworker', flat=True))
            user_list = User.objects.filter(user_id__in=users)
            return [(u, 0) for u in user_list]

        recipients=[]
        for i, recipient in enumerate(self.recipients.split(',')):
            if recipient.isdigit():
                group_list = list(Group.objects.get(id=recipient).user_set.all())
                recipients = recipients + [(u,i) for u in group_list]                 
                continue

            recipient_real = self.rgetattr(obj,recipient)
            if recipient_real:
                if type(recipient_real) == int:
                    user = User.objects.filter(user_id=recipient_real).first()
                    if user: recipients.append((user,i))
                else:
                    recipients.append((recipient_real,i))
                
        return recipients
    
    #get senders in User name.
    def get_senders(self,obj=None):
        if self.senders == 'System':
            return 'System'
        if self.senders.isdigit(): 
            return User.objects.filter(user_id=int(self.senders)).first()
        else:
            custom_user = self.rgetattr(obj,self.senders)
            if type(custom_user) == int:
                return User.objects.filter(user_id=custom_user).first()
            else:
                return custom_user

    #get action object user.
    def get_action_user(self,reciepient,obj=None):
        if self.action_user:
            if self.action_user == "same":
                return reciepient
            elif self.action_user == "escalated_user" :
                return None #handled at the time of notification creation
            return self.rgetattr(obj,self.action_user)
        return None

    #for replace wildcards
    def rgetattr(self,obj, attr, *args):
        if obj:
            def _getattr(obj, attr):
                if type(obj) == dict:
                    return obj.get(attr,"")
                else:
                    return getattr(obj, attr, *args)
                    
            return functools.reduce(_getattr, [obj] + attr.split('-'))
        return None
        
    #remove wildcards and replace with actual data
    def replace(self,text,obj):
        if text and obj:
            keywords = re.findall('{(.+?)}',text)
            replacements={}
            for keyword in keywords:
                item = keyword
                include_time_resolution = False
                try:
                    if '|time' in keyword:
                        item = keyword.split('|time')[0]
                        include_time_resolution = True

                    attr_value = self.rgetattr(obj,item)
                    if attr_value and type(attr_value) == datetime.datetime:
                        tz_offset = eval(Data.c_value("CLIENT_TIMEZONE")) if Data.c_value("CLIENT_TIMEZONE") else 0
                        attr_value = attr_value + datetime.timedelta(minutes=tz_offset)
                        if include_time_resolution:
                            attr_value = attr_value.strftime('%d %b %Y, %H:%M')
                        else:
                            attr_value = attr_value.date().strftime('%d %b %Y')

                    replacements.update({keyword:attr_value})

                except Exception: #In case values cannot be found
                    replacements.update({keyword:"< >"})

            return text.format(**replacements)
        else:
            return ""

    def actual_verb(self,obj):
        return self.replace(self.verb,obj)

    def actual_link(self,obj):
        return self.replace(self.link,obj)

    def actual_description(self,obj):
        return self.replace(self.description,obj)

    def event_date(self,obj,idx,offset_days):
        event_date = None
        if obj and self.event_date_field:
            event_date = self.rgetattr(obj, self.event_date_field)

        # For Respond by coming in from log request
        if type(event_date) == str :
            event_date = datetime.datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)

        try:
            off_set = int(offset_days[idx])
        except IndexError:
            off_set = 0
            
        if event_date:
            respond_by = event_date - datetime.timedelta(off_set)
            if respond_by < timezone.now():
                respond_by = timezone.now() + datetime.timedelta(hours=1)    # Check if respond by is less than today. If yes, set the respond by as 1 hr from now.
        else:
            respond_by = timezone.now() + datetime.timedelta(hours=1)

        return respond_by

class Rule(models.Model):
    rule_id = models.AutoField(primary_key=True)
    filter = models.CharField(max_length=200, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True) #app.model.field
    value = models.CharField(max_length=200, blank=True, null=True) # now, today, <int>
    
    #For date comparison:
    # old date ( training completed date): thresould > 0
    # future date (visa expiry): threshold < 0
    #For numbers:
    #  as usual
    # NOTE that this only happens for rule thresholds.
    # For notification thresholds it always positive
    threshold = models.CharField(max_length=200, blank=True, null=True)
    rule_name = models.CharField(max_length=100, blank=True, null=True)

    #if comparison:
    # always > for dates ^^^  
    condition = models.CharField(max_length=5, blank=True, null=True)
    related_trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE, related_name="related_trigger", blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')

    OPS = {'=': operator.eq, '>': operator.gt, '<': operator.lt}

    class Meta:
        managed = True
        db_table = 'hcms_alerts_rules'
        verbose_name = 'Lead Time'


    def field_value_by_id(self,obj,no):
        return getattr(obj,self.field_name_by_id(no))

    def app_label_by_id(self,no):
        return self.field.split(',')[no].split('.')[0] 

    def model_name_by_id(self,no):
        return self.field.split(',')[no].split('.')[1]

    def field_name_by_id(self,no):
        return self.field.split(',')[no].split('.')[2]

    def get_filter_by_id(self,no):
        return json.loads(self.filter)[no]

    def class_name_by_id(self,no):
        return apps.get_model(app_label=self.app_label_by_id(no), model_name=self.model_name_by_id(no))

    def threshold_by_id(self,no):
        return self.threshold.split(",")[no]

    def get_objects_for_filed(self,field_no):
        obs=self.class_name_by_id(field_no).objects.filter()
        
        ##assumption:all fields should be in same table
        if self.related_trigger: #if not a elavated notification objects aka fresh
            #taking existing notification objects related to rule label
            existing_notification_list=[o.action_object.pk for o in Notification.objects.filter(notification_label=self.related_trigger.label)]
            obs=self.class_name_by_id(field_no).objects.exclude(pk__in=existing_notification_list) #avoid the objects if it has been already notified

        kwargs=self.get_filter_by_id(field_no)
        if kwargs:
            Qr = None
            for key, value in kwargs.items():
                q = ~Q(**{key[1:]:value}) if key.startswith("~") else Q(**{key:value}) # exlude the negations
                if Qr :
                    Qr = Qr & q 
                else:
                    Qr = q
            return obs.filter(Qr)
        return obs

    def objects_to_check(self):
        objects=[]
        #todo:this doesnt need to be done. all the fields get the same set of objects
        for i in range(len(self.field.split(","))):
            objects.append(self.get_objects_for_filed(i))
        return objects
        
    def parsed_value_by_id(self,no):
        value=self.value.split(',')[no]
        if value=="now":
            return timezone.now()
        elif value=="today":
            return timezone.now().date()
        else:
            return int(value)
    
    def condition_by_id(self,no):
        return self.condition.split(",")[no]

    #threshold is in days
    #function is: <compare_value> - <field_value > <condition> <thresold>
    #         eg:      now        -   visa expiry      >        3  
    def threshold_exceeds(self,obj,threshold,no):
        field_value = self.field_value_by_id(obj,no) #extract field value from objectec #aka timestamp
        
        if not field_value:
            return False
        compare_value = self.parsed_value_by_id(no) #aka now/today/value
        condition = self.condition_by_id(no)
        print("field_value",field_value,"compare_value",compare_value)
        if isinstance(field_value,int):
            diff=compare_value-field_value
        elif isinstance(field_value,datetime.datetime):
            diff=(compare_value.replace(tzinfo=timezone.utc)-field_value.replace(tzinfo=timezone.utc)).total_seconds()/60
        print("diff=",str(diff),condition,"threshold=",threshold)
        return self.OPS[condition](diff,threshold)

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    PRIMARY = 0
    SECONDARY = 1
    EVLEVATIONS = 2
    notification_id = models.AutoField(primary_key=True)
    info_trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE, related_name="trigger_map", blank=True, null=True) #store related information
    current_trigger_id = models.IntegerField(blank=True, null=True)
    
    notification_label=models.CharField(max_length=50, blank=True, null=True)
    notification_status_mc_id = models.SmallIntegerField(blank=True, null=True) #NOTIFICATION_STATUS: Closed, Elevated, Halted, New
    notification_type_mc_id = models.SmallIntegerField(blank=True, null=True) #NOTIFICATION_TYPE : Alert, Notification Reminder Request,

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='recipient_notification',
        on_delete=models.CASCADE
    )
    action_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='action_user_notification',
        on_delete=models.CASCADE
    )
    origin_notification = models.ForeignKey("self",on_delete=models.CASCADE,blank=True, null=True)
    
    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='notify_action_object', on_delete=models.CASCADE)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')
    
    seen_date = models.DateTimeField(blank=True, null=True) #seen datetime if available

    remind_on = models.DateTimeField(blank=True, null=True) 
    remind_comment = models.TextField(blank=True, null=True) 

    event_date = models.DateTimeField(blank=True, null=True) #seen datetime if available
    subtype = models.SmallIntegerField(blank=True, null=True) #0 primary, 1 secondary(to avoid elevation for 1st time notificaitonss), 2 elevations
    closure_value = models.CharField(max_length=200, blank=True, null=True)
    closed_by = models.IntegerField(blank=True, null=True)
    closed_date = models.DateTimeField(blank=True, null=True)
    closure_type_mc_id = models.SmallIntegerField(blank=True, null=True) #NOTIFICATION_CLOUSURE_TYPE: Auto, Force, Runout
    closure_reason = models.CharField(max_length=200, blank=True, null=True)
    is_unresolved = models.BooleanField(default=False)
    emailed=models.BooleanField(blank=False, null=True) 
    
    timestamp = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')
    
    class Meta:
        managed = True
        db_table = 'hcms_alerts_notification'

    @property
    def reminder(self):        
        return Trigger.objects.filter(trigger_id=self.current_trigger_id).first()

    # @property
    # def event_date(self):
    #     if self.action_object and self.info_trigger.event_date_field:
    #         return self.rgetattr(self.action_object,self.info_trigger.event_date_field)

    #for replace wildcards
    def rgetattr(self,obj, attr, *args):
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)
        return functools.reduce(_getattr, [obj] + attr.split('-'))

    # @property
    # def url(self):
    #     if self.info_trigger.url:
    #         return self.info_trigger.replace(self.info_trigger.url,self.notification.action_object)

    @property
    def verb(self):
        if self.info_trigger.verb:
            return self.info_trigger.actual_verb(self.action_object)

    @property
    def description(self):
        desc = None
        if self.info_trigger.description:
            desc = self.info_trigger.actual_description(self.action_object)
            if self.info_trigger.action_user == 'escalated_user':
                desc = '%s(%s): %s' % (self.action_user.profile.surname,
                                      self.action_user.group_short,
                                      desc)
        return desc

    # +/- value is returned
    # + future events
    # - past events 
    @property
    def priority(self):
        if self.info_trigger.event_date_field:
            return (self.event_date()- timezone.now()).days

    @property
    def auto_closure_value(self):
        field=self.info_trigger.closure_field
        if field:
            clousure_value = getattr(self.action_object,field.split("__")[1])
            return clousure_value
        return None

    def close_associated_notifications(self,dismiss_secondary = True):

        ass_notifications = Notification.objects.filter(origin_notification_id=self.notification_id)

        if not dismiss_secondary:
            ass_notifications.exclude(subtype = Notification.SECONDARY)
            
        ass_notifications.update(
            closure_type_mc_id = Data.code("NOTIFICATION_CLOUSURE_TYPE","Auto"), # clouser type is Auto
            closure_reason = "Dismiss",
            closed_date = timezone.now(),
            notification_status_mc_id = Data.code("NOTIFICATION_STATUS","Closed") # set notification to closed
        )

        #roster_spl_handling
        if self.info_trigger.label == 'roster_notify_cw':
            related_notifications = list(Notification.objects.filter(Q(origin_notification_id=self.notification_id) |
                                                        Q(origin_notification_id=self.origin_notification)).values_list(
                                                                      'origin_notification_id', flat=True))

            associated_roster_notif = Notification.objects.filter(action_user = self.action_user, action_object_object_id__in = related_notifications )
            associated_roster_notif.update(
                closure_type_mc_id=Data.code("NOTIFICATION_CLOUSURE_TYPE", "Auto"),  # clouser type is Auto
                closure_reason="Dismiss",
                closed_date = timezone.now(),
                notification_status_mc_id=Data.code("NOTIFICATION_STATUS", "Closed")  # set notification to closed
            )

        return ass_notifications

    def set_seen(self, requester):
        sync_not = []
        self.seen_date = timezone.now()
        seen_closure_enabled = self.info_trigger.seen_closure
        status = self.notification_status_mc_id
        if seen_closure_enabled and self.seen_date and (not status ==  Data.code("NOTIFICATION_STATUS","Closed")):
            current_closure_value = 1 #since its always seen
            self.closure_type_mc_id = Data.code("NOTIFICATION_CLOUSURE_TYPE","Auto") # clouser type is Auto
            self.closed_by = requester.user_id
            self.closure_reason="Seen"
            self.notification_status_mc_id = Data.code("NOTIFICATION_STATUS","Closed") # set notification to closed
            self.close_associated_notifications(dismiss_secondary = False)
            self.closed_date = timezone.now()
            self.save()


            from api import signals
            signals.make_followups(self, current_closure_value)
            
            #close origin if applicable
            ass_notifications = Notification.objects.filter(notification_id = self.origin_notification_id)
            for a_notification in ass_notifications:
                if a_notification.info_trigger.seen_closure:
                    a_notification.closure_type_mc_id = Data.code("NOTIFICATION_CLOUSURE_TYPE","Auto") # clouser type is Auto
                    a_notification.closure_reason = "Seen"
                    a_notification.closed_by = requester.user_id
                    a_notification.closed_date = timezone.now()
                    a_notification.notification_status_mc_id = Data.code("NOTIFICATION_STATUS","Closed") # set notification to closed
                    a_notification.save()
                    signals.make_followups(a_notification, current_closure_value)
                    sync_not.append(a_notification)
        else:
            self.save()

        sync_not.append(self)
        return sync_not

    def unset_seen(self, requester):
        sync_notification = []
        seen_closure_enabled = self.info_trigger.seen_closure
        if seen_closure_enabled:
            return False, "Acknowledgement of this notification cannot be reverted"
        else:
            self.seen_date = None
            self.save()
            sync_notification.append(self)
            return True, sync_notification


class Followup(models.Model):
    followup_id = models.AutoField(primary_key=True)
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE, related_name="followup", blank=True, null=True) 
    next_triggers=models.CharField(max_length=200, blank=True, null=True) #next trigger to be made
    closure_type = models.SmallIntegerField(blank=True, null=True) #each closure type gets a followup

    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    last_modified_by = models.IntegerField(blank=True, null=True)
    delete_ind = models.CharField(max_length=1, default='N')


    class Meta:
        managed = True
        db_table = 'hcms_alerts_followup'

    
