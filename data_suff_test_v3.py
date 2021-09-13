#imports
from cw.models import EmploymentRecord
from su.models import SuWeeklyBooking
from django.db.models import Q
from pandas import date_range
from django.utils import timezone

def get_cw_skill (cwrecord, startdate, enddate):
    cw_skill = dict()
    for care_w in cwrecord:
        s = max(startdate, care_w.start_date, care_w.user.cw_skill.first().valid_from)
        if care_w.terminated_on:
            e = min(care_w.end_date, enddate, care_w.user.cw_skill.first().valid_to, care_w.terminated_on )
        else:
            e = min(care_w.end_date, enddate, care_w.user.cw_skill.first().valid_to) #include termination date
        period = date_range(start= s , end= e)
        is_wom = bool(care_w.user.profile.sex_mc_id == 8)
        skills = care_w.user.cw_skill.first().skills
        for p in period:
            day = p.date()
            cw_skill[day] = cw_skill.get(day, {'all': {}, 'fem': {}})
            for s in skills:
                cw_skill[day]['all'][s] = cw_skill[day]['all'].get(s, 0) + 1
                if is_wom:
                    cw_skill[day]['fem'][s] = cw_skill[day]['fem'].get(s, 0) + 1
    return cw_skill

def booking_info(subooking,startdate,enddate ):
    week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    bm_dict = {}
    for booking in subooking:
        s = max(startdate, booking.valid_from)
        if booking.service_user.care_plan.first().termination_date :
            e = min(booking.valid_to, enddate ,booking.service_user.care_plan.first().termination_date)
        else:
            e = min(booking.valid_to, enddate)
        period = date_range(start = s, end=e,freq='W-' + str(week[booking.day_of_the_week])) # termination date, careplan date
        is_wom = bool(booking.service_user.profile.sex_mc_id == 8)
        st_hr = booking.start_time.hour
        end_hr = booking.end_time.hour
        skills = booking.skills_required
        for p in period:
            day = p.date()
            bm_dict[day] = bm_dict.get(day, {})
            for h in range(st_hr, end_hr + 1):
                bm_dict[day][h] = bm_dict[day].get(h, {'all': {}, 'fem': {}})
                for s in skills:
                    bm_dict[day][h]['all'][s] = bm_dict[day][h]['all'].get(s, 0) + booking.no_of_cw
                    if is_wom:
                        bm_dict[day][h]['fem'][s] = bm_dict[day][h]['fem'].get(s, 0) + booking.no_of_cw
    return bm_dict

def check_insuff(bm_dict ,cw_skill ):
    insuff = {'all': [], 'fem': []}
    for date in bm_dict:
        if date not in cw_skill.keys():
            print('No cw available on ', date, ' Required cw and skills ', bm_dict[date])
            continue
        for h in bm_dict[date]:
            for skill in bm_dict[date][h]['all']:
                if skill not in cw_skill[date]['all'].keys():
                    print('No cw for day ', date, ' hour ', h, ' skill ', skill)
                elif cw_skill[date]['all'][skill] >= bm_dict[date][h]['all'][skill]:
                    continue
                insuff['all'].append(
                    (date, h, skill, bm_dict[date][h]['all'][skill] - cw_skill[date]['all'].get(skill, 0)))
            for skill in bm_dict[date][h]['fem']:
                if skill not in cw_skill[date]['fem'].keys():
                    print('No female cw for day ', date, ' hour ', h, ' skill ', skill)
                elif cw_skill[date]['fem'][skill] >= bm_dict[date][h]['fem'][skill]:
                    continue
                insuff['fem'].append(
                    (date, h, skill, bm_dict[date][h]['fem'][skill] - cw_skill[date]['fem'].get(skill, 0)))
    return insuff

now = timezone.now()
startdate = now.replace(day = 13, month = 11, year = 2020 ) #'2020-11-13 04:30:00'
enddate = now.replace(day = 13, month = 12, year = 2020 )# '2020-12-13 05:29:59'

cwemploy = EmploymentRecord.objects.filter( employment_status = 725 )
cwemploy = cwemploy.filter(Q( terminated_on__gte = startdate) | Q( terminated_on__isnull = True))
cwemploy = cwemploy.exclude(employment_contract_type_mc_id = 1111 )
cwemploy = cwemploy.exclude(Q(end_date__lt = startdate)| Q(  start_date__gt = enddate))
cwemploy = cwemploy.exclude( Q(user__cw_skill__valid_from__gte = enddate)| Q( user__cw_skill__valid_to__lte = startdate))

cw_skill = get_cw_skill(cwemploy, startdate, enddate)

subooking = SuWeeklyBooking.objects.exclude(Q(valid_to__lt = startdate) | Q(valid_from__gt = enddate))
subooking = subooking.exclude( Q(service_user__care_plan__start_date__gt = enddate) | Q( service_user__care_plan__end_date__lt = startdate ))
#subooking = subooking.filter(Q(service_user__care_plan__termination_date__gte = enddate) | Q(service_user__care_plan__termination_date__isnull = True))
subooking = subooking.exclude(Q(service_user__care_plan__termination_date__lte = startdate) )

bm_dict = booking_info(subooking,startdate,enddate )

##test

is_suf = check_insuff(bm_dict, cw_skill)

if len(is_suf['all']):
    print('Insufficient cw for all genders ', is_suf['all'])
else:
    print('For all genders data is sufficient')

if len(is_suf['fem']):
    print('Insufficient cw for women ', is_suf['fem'])
else:
    print('For women data is sufficient')


