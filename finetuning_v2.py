import numpy as np

from cw.models import EmploymentRecord
from cw.models import HcmsCwPreference
from cw.models import Certificate
from cw.models import AvailabilitySlot
from cw.models import SkillTemplate
from su.models import SuWeeklyBooking
from su.models import HcmsSuPreference
from su.models import CWException
from su.models import CarePlan
from booking.models import ScheduledBooking
from booking.models import BookingAllocationQuality
from django.db.models import Q, F
from pandas import date_range
from django.utils import timezone
from datetime import time, timedelta


def get_period_of_consideration():
    """ returns start date and end date to the period of consideration"""
    now = timezone.now()
    start = now.replace(day=13, month=11, year=2020)  # '2020-11-13 04:30:00'
    end = now.replace(day=start.day, month=start.month + 1, year=start.year)  # '2020-12-13 05:29:59'
    return start, end


def cw_in_period(startdate, enddate):
    """takes the start and end date of the period as input
    gives the cw info (employment info and certificate info) for valid cw during period as output"""
    cwemploy = EmploymentRecord.objects.exclude(employment_contract_type_mc_id=1111)  ###
    cwemploy = cwemploy.exclude(Q(end_date__lt=startdate) | Q(start_date__gt=enddate))  ####
    cwemploy = cwemploy.filter(Q(terminated_on__gte=startdate) | Q(terminated_on__isnull=True))
    cwemploy = cwemploy.filter(employment_status=725)
    cwemploy_users = cwemploy.values_list('user__user_id', flat=True)
    cw_cert = Certificate.objects.filter(user__user_id__in=cwemploy_users)
    cw_slots = AvailabilitySlot.objects.filter(cw_availability__user__user_id__in=cw_cert.values_list('user__user_id', flat=True))
    return cw_slots


def booking_in_period(startdate, enddate):
    """takes the start and end date of the period as input
    gives booking info (booking details and care plan details) for valid bookings and care plans in the period"""
    subooking = SuWeeklyBooking.objects.exclude(Q(valid_to__lt=startdate) | Q(valid_from__gt=enddate))
    sucareplan = CarePlan.objects.exclude(termination_date__lte=startdate)
    sucareplan = sucareplan.exclude(Q(end_date__lt=startdate) | Q(start_date__gt=enddate))
    subooking = subooking.filter(service_user__user_id__in = sucareplan.values_list('user_id', flat=True))
    return subooking


def get_eligible_bookings_for_day_slot(booking_records, bk_not_overnight_on_day, bk_overnight_on_day,bk_overnight_on_prev_day,  slot):  ####
    """takes booking and care plan info
    """
    #bm.annotate(is_overnight= ((F('start_time') - F('end_time'))))
    #for bk in bm:
    #    bk.is_overnight = bk.is_overnight.days > 0
    # bookings on day (not overnight)
    bk_not_overnight_on_day = bk_not_overnight_on_day.exclude(Q(start_time__gt =  slot[1])| Q(end_time__lt = slot[0]))
    # bookings on day (overnight)
    if slot[0].hour >= 12:
        bm_ovnt_onday = bk_overnight_on_day.filter(start_time__lte = slot[0])
        overnight_onday  = 1
    else:
        overnight_onday  = 0
    #bookings overnight (spill over of previous day)
    if slot[0].hour <12:
        bm_ovnt_prev_day = bk_overnight_on_prev_day.filter(end_time__gte = slot[1])
        overnight_prevday = 1
    else:
        overnight_prevday = 0
    ##
    if overnight_prevday and overnight_onday :
        bm_final = booking_records.filter(Q(weekly_booking_id__in = bk_not_overnight_on_day.values_list('weekly_booking_id', flat=True) ) |
                         Q(weekly_booking_id__in = bm_ovnt_onday.values_list('weekly_booking_id', flat=True))|
                         Q(weekly_booking_id__in=bm_ovnt_prev_day.values_list('weekly_booking_id', flat=True)))
    elif overnight_onday:
        bm_final = booking_records.filter(
            Q(weekly_booking_id__in=bk_not_overnight_on_day.values_list('weekly_booking_id', flat=True)) |
            Q(weekly_booking_id__in=bm_ovnt_onday.values_list('weekly_booking_id', flat=True)) )
    elif overnight_prevday:
        bm_final = booking_records.filter(
            Q(weekly_booking_id__in=bk_not_overnight_on_day.values_list('weekly_booking_id', flat=True)) |
            Q(weekly_booking_id__in=bm_ovnt_prev_day.values_list('weekly_booking_id', flat=True)))
    else:
        bm_final = booking_records.filter(
            Q(weekly_booking_id__in=bk_not_overnight_on_day.values_list('weekly_booking_id', flat=True)))
    return bm_final


def get_eligible_cw_for_day_slot(cw_slot,  slot):  #####
    """takes cw skill certificate and cw employment info and date in period
    returns the cw who have valid contracts on that date """
    cw_in_slot = cw_slot.exclude(Q(started_time__gt=slot[1]) | Q(finished_time__lt=slot[0]))
    return cw_in_slot


def get_bm_with_skill(bm_rec, skill):
    bm_final = bm_rec.filter(skills_required__contains = [skill])
    return bm_final


def get_cw_with_skill(cw_rec , skill):
    cw = cw_rec.filter(cw_availability__user__cw_skill__skills__contains=[skill])
    return cw


def get_sol_dict_template():
    sol = {
        0: {'cw avail': {'gen': [0] * 24, 'fem': [0] * 24}, 'insuff': {'skills': {}, 'gender': {'gen': [], 'fem': []}}},
        1: {'cw avail': {'gen': [0] * 24, 'fem': [0] * 24}, 'insuff': {'skills': {}, 'gender': {'gen': [], 'fem': []}}},
        2: {'cw avail': {'gen': [0] * 24, 'fem': [0] * 24}, 'insuff': {'skills': {}, 'gender': {'gen': [], 'fem': []}}},
        3: {'cw avail': {'gen': [0] * 24, 'fem': [0] * 24}, 'insuff': {'skills': {}, 'gender': {'gen': [], 'fem': []}}},
        4: {'cw avail': {'gen': [0] * 24, 'fem': [0] * 24}, 'insuff': {'skills': {}, 'gender': {'gen': [], 'fem': []}}},
        5: {'cw avail': {'gen': [0] * 24, 'fem': [0] * 24}, 'insuff': {'skills': {}, 'gender': {'gen': [], 'fem': []}}},
        6: {'cw avail': {'gen': [0] * 24, 'fem': [0] * 24}, 'insuff': {'skills': {}, 'gender': {'gen': [], 'fem': []}}}}
    return sol


def get_all_skill():
    all_skill = SkillTemplate.objects.values_list('skill_template_id', flat=True)
    return all_skill


def get_slots():
    """returns a list of tuples where each tuple has the start time of the slot
    and the end time of the slot (inclusive)"""
    slots = [(time(0, 0, 0), time(0, 59, 59)), (time(1, 0, 0), time(1, 59, 59)), (time(2, 0, 0), time(2, 59, 59)),
             (time(3, 0, 0), time(3, 59, 59)), (time(4, 0, 0), time(4, 59, 59)), (time(5, 0, 0), time(5, 59, 59)),
             (time(6, 0, 0), time(6, 59, 59)), (time(7, 0, 0), time(7, 59, 59)), (time(8, 0, 0), time(8, 59, 59)),
             (time(9, 0, 0), time(9, 59, 59)),
             (time(10, 0, 0), time(10, 59, 59)), (time(11, 0, 0), time(11, 59, 59)), (time(12, 0, 0), time(12, 59, 59)),
             (time(13, 0, 0), time(13, 59, 59)), (time(14, 0, 0), time(14, 59, 59)), (time(15, 0, 0), time(15, 59, 59)),
             (time(16, 0, 0), time(16, 59, 59)), (time(17, 0, 0), time(17, 59, 59)), (time(18, 0, 0), time(18, 59, 59)),
             (time(19, 0, 0), time(19, 59, 59)), (time(20, 0, 0), time(20, 59, 59)), (time(21, 0, 0), time(21, 59, 59)),
             (time(22, 0, 0), time(22, 59, 59)), (time(23, 0, 0), time(23, 59, 59))]
    return slots


def advanced_sufficiency(cw_record, bm):
    """take into consideration has pets, is a smoker, sex, religion, ethnicity, primary language,
    hard preferences"""
    alloc_qual = BookingAllocationQuality.objects.filter(booking__weekly_booking_id=bm.weekly_booking_id)
    if len(alloc_qual):
        alloc_qual = alloc_qual.exclude(Q(is_cw_hard_failed=True) | Q(is_su_hard_failed=True))
        cw_alloc_qual = alloc_qual.values_list('careworker', flat=True).distinct()
        cw_record = cw_record.filter(user__user_id__in=cw_alloc_qual)
    #
    else:
        # remove cw who do not fit into su's hard pref
        su_pref = HcmsSuPreference.objects.filter(user__user_id=bm.service_user.user_id, incorporation_type_mc_id=662)
        for su_record in su_pref:
            if su_record.preference_type_mc_id == 661:
                cw_record = cw_record.filter(
                    user__profile__primary_language_mc_id=bm.service_user.profile.primary_language_mc_id)
            elif su_record.preference_type_mc_id == 660:
                cw_record = cw_record.filter(user__profile__ethnicity_mc_id=bm.service_user.profile.ethnicity_mc_id)
            elif su_record.preference_type_mc_id == 659:
                cw_record = cw_record.filter(user__profile__religion_mc_id=bm.service_user.profile.religion_mc_id)
            elif su_record.preference_type_mc_id == 657:
                cw_record = cw_record.filter(user__profile__sex_mc_id=bm.service_user.profile.sex_mc_id)
            elif su_record.preference_type_mc_id == 658:
                su_except = CWException.objects.filter(user__user_id=su_record.user.user_id).values_list('exceptions')
                z = []
                if len(su_except) != 0:
                    y = [x for x in su_except][0][0].split(',')
                else:
                    y = []
                for w in y:
                    z.append(w)
                cw_record = cw_record.exclude(user__user_name__in=z)
        # remove cw who have hard pref conflicting with su
        cw_w_hard_pref = HcmsCwPreference.objects.filter(
            user__user_id__in=cw_record.values_list('user__user_id', flat=True))
        cw_w_hard_pref = cw_w_hard_pref.filter(incorporation_type_mc_id=662)
        for cw_indiv in cw_w_hard_pref:
            if cw_indiv.preference_type_mc_id == 661 and cw_indiv.user.profile.primary_language_mc_id != bm.service_user.profile.primary_language_mc_id:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 660 and cw_indiv.user.profile.ethnicity_mc_id != bm.service_user.profile.ethnicity_mc_id:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 659 and cw_indiv.user.profile.religion_mc_id != bm.service_user.profile.religion_mc_id:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 657 and cw_indiv.user.profile.sex_mc_id != bm.service_user.profile.sex_mc_id:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 656 and bm.service_user.profile.is_non_smoker == 0:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 260 and bm.service_user.serviceuser.has_no_pets == 0:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 665 and bm.booking_type_mc_id in [int(x) for x in
                                                                                     cw_indiv.preference_value.split(
                                                                                             ',')]:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
    return cw_record


def update_solution_gender(sol, bm_day, slot, insuff, is_wom):
    """updates the insufficiency list when the insufficiency is detected
    returns the updated insufficiency list"""
    if is_wom:
        sol[bm_day]['insuff']['gender']['fem'].append((slot, insuff))
    else:
        sol[bm_day]['insuff']['gender']['gen'].append((slot, insuff))
    return sol


def update_solution_skill(sol, bm_day, slot, skill, insuff, is_wom):
    """updates the insufficiency list when the insufficiency is detected
    returns the updated insufficiency list"""
    sol[bm_day]['insuff']['skills'][skill] = sol[bm_day]['insuff']['skills'].get(skill, {'gen': [], 'fem': []})
    if is_wom:
        sol[bm_day]['insuff']['skills'][skill]['fem'].append((slot, insuff))
    else:
        sol[bm_day]['insuff']['skills'][skill]['gen'].append((slot, insuff))
    return sol


def is_fine_tune_insuff( cw_slots, bm_record):
    """check whether there exist insufficiency in the period of consideration for valid bookings and care workers"""
    sol = get_sol_dict_template()
    # slot information
    slots = get_slots()
    #skills
    all_skills = get_all_skill()
    # set ending of the bookings of h:00:00 to h-1:59:59 to make insufficiency calculation easier
    for bk in bm_record:
        if bk.end_time.minute == 00 and bk.end_time.second == 00:
            bk.end_time = time(bk.end_time.hour - 1, 59, 59)
            bk.save()
    for cw_indiv in cw_slots:
        if cw_indiv.finished_time.minute == 00 and cw_indiv.finished_time.second == 00:
            cw_indiv.finished_time = time((cw_indiv.finished_time.hour - 1) % 24, 59, 59)
            cw_indiv.save()
    # iterate through all dates in the range to check insufficiency on each
    bm_not_overnight = bm_record.filter(end_time__gt=F('start_time'))
    bm_overnight = bm_record.filter(end_time__lt=F('start_time'))
    # careworkers valid
    d,sl,sk = timedelta(0,0,0),timedelta(0,0,0),timedelta(0,0,0)
    for day in range(7):
        s_day = timezone.now()
        cw_on_day = cw_slots.filter(day_of_week=day)
        bm_not_overnight_on_day = bm_not_overnight.filter(day_of_the_week = day)
        bm_overnight_on_day = bm_overnight.filter(day_of_the_week = day)
        bm_overnight_on_prev_day = bm_overnight.filter(day_of_the_week = (day-1)%7)
        for slot in slots:
            s_slot = timezone.now()
            cw_in_slot = get_eligible_cw_for_day_slot(cw_on_day,  slot)
            bm_in_slot = get_eligible_bookings_for_day_slot(bm_record , bm_not_overnight_on_day, bm_overnight_on_day, bm_overnight_on_prev_day, slot)
            if len(cw_in_slot) or len(bm_in_slot):
                num_cw_in_slot = len(cw_in_slot.distinct('cw_availability__user__user_id'))
                sol[day]['cw avail']['gen'][slot[0].hour] = [slot[0].hour, num_cw_in_slot]
                sol[day]['cw avail']['fem'][slot[0].hour] = [slot[0].hour, len(cw_in_slot.filter(
                    cw_availability__user__profile__sex_mc_id=8).distinct('cw_availability__user__user_id'))]
                for skill in all_skills:
                    s_skill = timezone.now()
                    cw_slot_skill = get_cw_with_skill(cw_in_slot , skill)
                    bm_slot_skill = get_bm_with_skill(bm_in_slot, skill)
                    if len(cw_slot_skill) or len(bm_slot_skill):
                        num_cw_in_slot_w_skill = len(cw_slot_skill.distinct('cw_availability__user__user_id'))
                        num_cw_req_in_slot_w_skill = sum([x.no_of_cw for x in bm_slot_skill])
                        num_fem_cw_in_slot_w_skill = len(cw_slot_skill.filter(cw_availability__user__profile__sex_mc_id = 8).distinct('cw_availability__user__user_id'))
                        num_req_fem_cw_in_slot_w_skill = sum([x.no_of_cw for x in bm_slot_skill.filter(service_user__profile__sex_mc_id=8)])
                        if num_cw_in_slot_w_skill < num_cw_req_in_slot_w_skill:
                            sol = update_solution_skill(sol, day, slot, skill,  num_cw_req_in_slot_w_skill - num_cw_in_slot_w_skill , is_wom = False)
                        if num_fem_cw_in_slot_w_skill < num_req_fem_cw_in_slot_w_skill:
                            sol = update_solution_skill(sol, day, slot, skill,
                                                num_req_fem_cw_in_slot_w_skill - num_fem_cw_in_slot_w_skill, is_wom=True)
                    e_skill = timezone.now()
                    sk = max(sk, e_skill - s_skill)
            e_slot = timezone.now()
            sl = max(sl , e_slot - s_slot)
        sol[day]['cw avail']['gen'].sort(key=lambda x: x[1])  # key = lambda x:x[1]
        sol[day]['cw avail']['fem'].sort(key=lambda x: x[1])  # key = lambda x:x[1]
        print('day:  ', day)
        e_day = timezone.now()
        d = max(d , e_day - s_day)
    # sort result by the num of insuff
    ##
    ##
    print( 'time for day : ', d)
    print('time for slot : ', sl)
    print('time for skill : ', sk)
    return sol


def get_new_cw_info():
    skill = [55, 76, 24]
    gender = 7
    cw = {'skills': skill, 'sex_id': gender}
    return cw


def get_single_slot(cw_assignment):
    assignment = [0,0,0,0,0,0,0]
    assignment[0] = [(cw_assignment[0][0][0][0] , cw_assignment[0][0][-1][-1] )]
    assignment[1] =[(cw_assignment[1][0][0][0], cw_assignment[1][0][-1][-1])]
    assignment[2] = [(cw_assignment[2][0][0][0], cw_assignment[2][0][-1][-1])]
    assignment[3] = [(cw_assignment[3][0][0][0], cw_assignment[3][0][-1][-1])]
    assignment[4] = [(cw_assignment[4][0][0][0], cw_assignment[4][0][-1][-1])]
    assignment[5] = [(cw_assignment[5][0][0][0], cw_assignment[5][0][-1][-1])]
    assignment[6] = [(cw_assignment[6][0][0][0], cw_assignment[6][0][-1][-1])]
    return assignment


def get_assignment(new_cw,  cw_slots,  subooking):
    assignment = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    insuff = is_fine_tune_insuff( cw_slots,  subooking)
    # sol[bm_day]['insuff']['skills'][skill]['fem'].append((slot, insuff))
    if (new_cw['sex_id'] == 8):
        gender = 'fem'
    else:
        gender = 'gen'
    if len(new_cw['skills']):
        for day in range(7):
            for s in insuff[day]['insuff']['skills']:
                if s in new_cw['skills']:
                    assignment[day].append([tup[0] for tup in insuff[day]['insuff']['skills'][s][gender]])
            for s in insuff[day]['insuff']['gender'][gender]:
                assignment.append({'day': day, 'slot': s[0]})
            if len(assignment[day]) == 0:
                assignment[day].append(
                    [(time(x[0], 0, 0), time(x[0], 59, 59)) for x in insuff[day]['cw avail'][gender][0:5]])
    else:
        print('Enter the skills in care worker record')
    return assignment, insuff


# set start and end dates of the period of consideration
startdate, enddate = get_period_of_consideration()
# select the cw who have valid contracts in the period of consideration
cw_slots = cw_in_period(startdate, enddate)
# select valid bookings for the period of consideration
subooking = booking_in_period(startdate, enddate)
cw_info = get_new_cw_info()
new_cw_assignment, insuff = get_assignment(cw_info, cw_slots, subooking)
for y in insuff:
    print(y)
    print(insuff[y]['cw avail'])
    print(insuff[y]['insuff'])
    print('----------')

new_cw_assignment = get_single_slot(new_cw_assignment)
print('Assignments: -----------')
for i in range(7):
    print(i)
    print(new_cw_assignment[i])

print('skills: -----------')
for x in insuff:
    print([y for y in insuff[x]['insuff']['skills']])



