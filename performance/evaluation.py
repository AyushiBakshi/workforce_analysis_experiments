from utils.models import Data
from django.db.models import Q
from cw.models import Leave, ChangeWeeklySchedule
from complaint.models import Feedback
from django.utils import timezone
import datetime
from performance.models import Criteria
from alerts.models import Notification
from booking.models import BookingAllocation


# class RequestChanges:
       
#    #gives leave frequency using dates within the range.
#    # range: "days" before today
#     def leave_frequency(user,days):
#         #get the date range: from today to "days" backward
#         to_date=datetime.date.today()
#         from_date=to_date - datetime.timedelta(days=days)

#         #approved leaves taken within range
#         on_leave_not_avail= Leave.objects.filter(
#                 Q(leave_status_mc_id__exact=Data.code("LEAVE_STATUS","Approved")) & 
#                 Q(user__exact= user) &
#                 Q(delete_ind__exact='N')
#             ).exclude(
#             ((Q(from_date__lte=from_date) & Q(to_date__lte=from_date)) |
#             (Q(from_date__gte=to_date) & Q(to_date__gte=to_date))) 
#         ).values_list('from_date','to_date')

#         leave_count=0
#         #Taking the count given date range.
#         for date1,date2 in on_leave_not_avail :
#             date1=date1.date()
#             date2=date2.date()
#             if date1 < from_date:
#                 date1=from_date
#             if date2 > to_date:
#                 date2=to_date
#             count=(date2 - date1).days +1 
#             leave_count= leave_count +  count

#         return leave_count/days

#     #gives cr count using created dates within the range.
#     # range: "days" before today
#     def cr_frequency(user,days):
#         #get the date range: from today to "days" backward
#         to_date=datetime.date.today()
#         from_date=to_date - datetime.timedelta(days=days)
        
#         #get the count of approved unavailable cr
#         cr_count= ChangeWeeklySchedule.objects.filter(
#                 Q(result_mc_id__exact=Data.code("CHANGE_SCHEDULE_RESULT","Approved")) & 
#                 Q(result_mc_id__exact=Data.code("CHANGE_SCHEDULE_STATUS","Unavailable")) & 
#                 Q(user__exact= user) &
#                 Q(created_date__range=(from_date,to_date)) &
#                 Q(delete_ind__exact='N')
#             ).count()
#         return cr_count/days



class Evaluation:
    
    # range: "days" before today #user object
    def feedback_evaluation(user,days):
        print()
        print("############FEEDBACK EVAL#############")
        #get the date range: from today to "days" backward
        to_date=to_date = timezone.now()
        from_date=to_date - datetime.timedelta(days=days)

        #get all the complaints and complements with given range
        feedbacks= Feedback.objects.filter(
                Q(about_user = user) &
                Q(feedback_status_mc_id__exact = Data.code("FEEDBACK_STATUS","Resolved")) &
                Q(created_date__range = (from_date,to_date)) &
                Q(delete_ind__exact = 'N')
            )
        
        external_feedback_count = 0
        external_total_val = 0

        internal_feedback_count = 0
        internal_total_val = 0
        for feedback in feedbacks:
            reported_user=feedback.from_user
            reported_user_group=reported_user.group
            score = feedback.feedback_score_level
            if reported_user_group == "Service User": #to do NOK
                criteria = Criteria.objects.get(criteria_type="feedback",criteria_sub_type="external",sub_type_match=score)
                external_total_val=external_total_val+criteria.sub_type_level
                external_feedback_count=external_feedback_count+1
                print("score",score,"level:",criteria.sub_type_level)
            else:
                criteria = Criteria.objects.get(criteria_type="feedback",criteria_sub_type="internal",sub_type_match=score)
                internal_total_val=internal_total_val+criteria.sub_type_level
                internal_feedback_count = internal_feedback_count + 1
                print("level:",criteria.sub_type_level)

        print(internal_feedback_count,internal_feedback_count)
        external_average_value = external_total_val/external_feedback_count if external_feedback_count else 0
        internal_average_value = internal_total_val/internal_feedback_count if internal_feedback_count else 0
        return {"external_feedback_score":external_average_value, "internal_feedback_score":internal_average_value}


    # range: "days" before today #user object
    def alert_response_evaluation(user,days):
        print()
        print("############ALERT ReSPONSE#############")
        #get the date range: from today to "days" backward
        to_date = timezone.now()
        from_date = to_date - datetime.timedelta(days=days)

        notifications = Notification.objects.filter(
            recipient = user,
            timestamp__range = (from_date,to_date),
            notification_status_mc_id__in=[Data.code("NOTIFICATION_STATUS","Closed"),Data.code("NOTIFICATION_STATUS","Halted")],
            origin_notification__isnull=True,
            delete_ind = 'N'
        )

        notification_count=notifications.count()
        total_val=0
        for notification in notifications:
            elavated_status = notification.reminder.seq
            notification_type = notification.notification_label
            criteria= Criteria.objects.filter(
                criteria_type="alert_response",
                criteria_sub_type=notification_type,
                sub_type_match=elavated_status
            ).first()
            if not criteria: continue
            print("level:","status=",elavated_status,criteria.sub_type_level)
            total_val=total_val+criteria.sub_type_level
            
        print("total",total_val,"count",notification_count)
        average_value = total_val/notification_count if notification_count else 0
        return {"alert_response_score":average_value }



    # range: "days" before today #user object
    def time_keeping_evaluation(user,days):
        print()
        print("############TIME KEEPING & DEPEND EVAL#############")
        #get the date range: from today to "days" backward
        to_date = timezone.now()
        from_date = to_date + datetime.timedelta(days=days) #change this inverse

        allocations = BookingAllocation.objects.filter(
            careworker = user.pk,
            booking__started_date_time__range = (to_date,from_date),
            booking__booking_status_mc_id=Data.code("BOOKING_STATUS","Past"),
            delete_ind = 'N'
        )
        allocation_count= allocations.count()

        noshow_total_val = 0
        noshow_count = 0

        late_total_val = 0
        late_count = 0

        print("---time length---")
        for allocation in allocations:
            
            #calculate no show count
            if allocation.service_start_status_mc_id == Data.code("SERVICE_START_STATUS","No Show"):
                noshow_count=noshow_count+1
            #calculate average late
            else:
                booking_time = allocation.booking.started_date_time
                service_time = allocation.service_start_date_time

                if not service_time: 
                    print("Warning: past booking has no service end time.")
                    continue

                diff = (service_time - booking_time).total_seconds() / 60
                if diff >= 0: #todo exclude lates less than 15min
                    criteria = Criteria.objects.filter(
                        criteria_type="time_keeping",
                        criteria_sub_type="length",
                        sub_type_match__lte=diff
                    ).order_by('-sub_type_seq').first() # to get the first match
                    if criteria:
                        late_total_val=late_total_val+criteria.sub_type_level
                        late_count=late_count+1
                        print("diff=",diff,"level",criteria.sub_type_level)

        #########################
        # Time keeping evaluation
        #########################

        #late length calculation
        average_length_level = late_total_val / late_count if late_count else 0


        print("---time count---")

        #late count calculation
        presentage_count = (late_count / allocation_count) * 100 if allocation_count else 0
        
        late_count_criteria = Criteria.objects.filter(
            criteria_type="time_keeping",
            criteria_sub_type="count",
            sub_type_match__lte=presentage_count,
        ).order_by('-sub_type_seq').first()  # to get the first match
        
        late_count_level =late_count_criteria.sub_type_level                      
        print("presentage=",presentage_count,"level",late_count_criteria.sub_type_level)



        #overall time_keep evalutaion
        overall_time_keep_eval = (average_length_level + late_count_level)/2

        ##########################
        # Dependabitlity evaluation
        ###########################
        print("---dependability---")

        #dependability calculation
        no_show_presentage = noshow_count/allocation_count * 100 if allocation_count else 0
        no_show_criteria = Criteria.objects.filter(
                    criteria_type="dependability",
                    criteria_sub_type="no_show",
                    sub_type_match__lte=no_show_presentage,
                ).order_by('-sub_type_seq').first()  # to get the first match
            
        no_show_level = no_show_criteria.sub_type_level
        print("presentage=",no_show_presentage,"level=",no_show_criteria.sub_type_level)

        return {"time_keeping_score":overall_time_keep_eval, "no_show_score":no_show_level}

class Weights:
    complaint_w = 10
    complement = -5
    leave_freq_w = 5
    cr_freq_w = 5
