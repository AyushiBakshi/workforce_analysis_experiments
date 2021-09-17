#Both set and dict (with query set)
#with required format

#imports
from cw.models import EmploymentRecord
from su.models import SuWeeklyBooking
from django.db.models import Q
from pandas import date_range
from django.utils import timezone
from datetime import time

#function that cw, booking info , start and end date of period of consideration and returns 2 sets
#sol: skill wise breakdown of insuff , sol_set: set wise breakdown of insuff
def is_insuff(cw_record, bm_record, startdate, enddate):
    week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    sol = []
    sol_set = []
    #go through each booking
    for booking in bm_record:
        req_skill = booking.skills_required
        req_cw = booking.no_of_cw
        st_hr = booking.start_time.hour
        end_hr = booking.end_time.hour
        d = booking.day_of_the_week
        s = max(startdate, booking.valid_from)
        if booking.service_user.care_plan.first().termination_date:
            e = min(booking.valid_to, enddate, booking.service_user.care_plan.first().termination_date)
        else:
            e = min(booking.valid_to, enddate)
        # get all the dates on which the booking lies, given the day of the week on which the booking falls
        bm_dates = date_range(start=s, end=e, freq='W-' + str(week[booking.day_of_the_week]))
        is_wom = bool(booking.service_user.profile.sex_mc_id == 8)
        # go through all the dates of the booking
        for date in bm_dates:
            # care worker
            avail_cw = cw_record.filter(Q(terminated_on__gt=date) | Q(terminated_on__isnull=True))
            avail_cw = avail_cw.filter(end_date__gte=date, start_date__lte=date)
            if is_wom:
                avail_cw = avail_cw.filter(user__profile__sex_mc_id=8)
            cw_skill = {}
            # booking
            same_skill_bm = bm_record.filter(service_user__care_plan__start_date__lte=date,
                                             service_user__care_plan__end_date__gte=date)
            same_skill_bm = same_skill_bm.filter(valid_to__gt=date, day_of_the_week=d)
            same_skill_bm = same_skill_bm.exclude(service_user__care_plan__termination_date__lte=date)
            same_skill_bm = same_skill_bm.exclude(Q(end_time__lt=time(st_hr, 0)) | Q(start_time__gt=time(end_hr, 0)))
            same_skill_bm = same_skill_bm.exclude(pk=booking.pk)
            # find whether each skill required in booking will be satisfied
            for skill in req_skill:
                if skill not in cw_skill.keys():
                    # create a dict of valid cw and req skills having format {skill: [user ids of cw having the skills], skill: ...}
                    cw_skill[skill] = avail_cw.filter(user__cw_skill__skills__contains=[skill]).values_list(
                        'user__user_id',
                        flat=True)
                ssbm = same_skill_bm.filter(skills_required__contains=[skill])
                # get the total num of cw required for the same skill in the same time other the booking in consideration
                sum_cw = sum([x.no_of_cw for x in ssbm])
                for h in range(st_hr, end_hr + 1):
                    if sum_cw + req_cw > len(cw_skill[skill]):
                        #if insufficient
                        insuff_skill = sum_cw + req_cw - len(cw_skill[skill])
                        # put the skill and insufficiency in proper format
                        in_sol = [x['date'] == date.date() for x in sol if len(sol)]
                        try:
                            i = in_sol.index(1)
                        except:
                            i = len(sol)
                            sol.append({'date': date.date(), 'slot_details': [
                                {'slot_time_start': h, 'slot_time_end': h + 1,
                                 'insufficiency': [{'skill_id': skill, 'female_skill_insufficiency': 0,
                                                    'overall_skill_insufficiency': insuff_skill}]}]})
                        in_sol = [x['slot_time_start'] == st_hr for x in sol[i]['slot_details'] if
                                  len(sol[i]['slot_details'])]
                        try:
                            j = in_sol.index(1)
                        except:
                            j = len(sol[i]['slot_details'])
                            sol[i]['slot_details'].append({'slot_time_start': h, 'slot_time_end': h + 1,
                                                           'insufficiency': [
                                                               {'skill_id': skill, 'female_skill_insufficiency': 0,
                                                                'overall_skill_insufficinecy': 0}]})
                        in_sol = [x['skill_id'] == skill for x in sol[i]['slot_details'][j]['insufficiency'] if
                                  len(sol[i]['slot_details'][j]['insufficiency'])]
                        try:
                            k = in_sol.index(1)
                        except:
                            k = len(sol[i]['slot_details'][j]['insufficiency'])
                            sol[i]['slot_details'][j]['insufficiency'].append(
                                {'skill_id': skill, 'female_skill_insufficiency': 0,
                                 'overall_skill_insufficiency': 0})
                        sol[i]['slot_details'][j]['insufficiency'][k]['overall_skill_insufficiency'] = max(
                            sol[i]['slot_details'][j]['insufficiency'][k]['overall_skill_insufficiency'], insuff_skill)
                        if is_wom:
                            sol[i]['slot_details'][j]['insufficiency'][k]['female_skill_insufficiency'] = max(
                                sol[i]['slot_details'][j]['insufficiency'][k]['female_skill_insufficiency'],
                                insuff_skill)
                # get the cw who have all of the skills in their skill set
                cw_for_all_skill = list(set.intersection(*[set(x) for x in cw_skill.values()]))
                num_cw_for_all_skill = len(cw_for_all_skill)
                # bookings competing with the entire required skill set
                same_skill_bm = same_skill_bm.filter(skills_required__contains=req_skill)
                req_cw_other_bm = sum([x.no_of_cw for x in same_skill_bm])
                if num_cw_for_all_skill - req_cw - req_cw_other_bm < 0:
                    # if insufficient
                    insuff = req_cw + req_cw_other_bm - num_cw_for_all_skill
                    sol_set.append({'date': date, 'hour': st_hr, 'required skill': req_skill, 'insufficiency': insuff,
                                    'user ids of avail cw': cw_for_all_skill, 'is su woman': is_wom})  # ,ssbm
    return sol, sol_set



#set start and end dates of the period of consideration
now = timezone.now()
startdate = now.replace(day=13,month=11,year=2020)#'2020-11-13 04:30:00'
enddate = now.replace(day=13,month=12,year=2020)#'2020-12-13 05:29:59'

#select the cw who have valid contracts in the period of consideration
cwemploy = EmploymentRecord.objects.filter(employment_status=725)
cwemploy = cwemploy.filter(Q(terminated_on__gte=startdate) | Q(terminated_on__isnull=True))
cwemploy = cwemploy.exclude(employment_contract_type_mc_id=1111)
cwemploy = cwemploy.exclude(Q(end_date__lt=startdate) | Q(start_date__gt=enddate))
cwemploy = cwemploy.exclude(Q(user__cw_skill__valid_from__gte=enddate) | Q(user__cw_skill__valid_to__lte=startdate))

#select valid bookings for the period of consideration
subooking = SuWeeklyBooking.objects.exclude(Q(valid_to__lt=startdate) | Q(valid_from__gt=enddate))
subooking = subooking.exclude(Q(service_user__care_plan__start_date__gt=enddate) | Q(service_user__care_plan__end_date__lt=startdate))
#subooking=subooking.filter(Q(service_user__care_plan__termination_date__gte=enddate)|Q(service_user__care_plan__termination_date__isnull=True))
subooking = subooking.exclude(service_user__care_plan__termination_date__lte=startdate)

insuff_skill_indiv, insuff_skill_set = is_insuff(cwemploy, subooking, startdate, enddate)

for x in insuff_skill_indiv:
    print(x)

