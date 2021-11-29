import numpy as np

from cw.models import EmploymentRecord
from cw.models import HcmsCwPreference
from cw.models import Certificate
from cw.models import AvailabilitySlot
from su.models import SuWeeklyBooking
from su.models import HcmsSuPreference
from su.models import CWException
from su.models import CarePlan
from booking.models import ScheduledBooking
from booking.models import BookingAllocationQuality
from django.db.models import Q
from pandas import date_range
from django.utils import timezone
from datetime import time, timedelta


def get_period_of_consideration():
    """ returns start date and end date to the period of consideration"""
    now = timezone.now()
    start = now.replace(day=13, month=11, year=2020)  # '2020-11-13 04:30:00'
    end = now.replace(day=start.day, month= start.month +1 , year=start.year)  # '2020-12-13 05:29:59'
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
    cw_slots = AvailabilitySlot.objects.filter(cw_availability__user__user_id__in=cwemploy_users)
    return cwemploy, cw_cert, cw_slots


def booking_in_period(startdate, enddate):
    """takes the start and end date of the period as input
    gives booking info (booking details and care plan details) for valid bookings and care plans in the period"""
    subooking = SuWeeklyBooking.objects.exclude(Q(valid_to__lt=startdate) | Q(valid_from__gt=enddate))
    sucareplan = CarePlan.objects.exclude(termination_date__lte=startdate)
    sucareplan = sucareplan.exclude(Q(end_date__lt=startdate) | Q(start_date__gt=enddate))
    return subooking, sucareplan


def get_eligible_bookings_on_day(booking_records, careplan_records, day):
    """takes booking and care plan info and date in period
    returns the bookings which exist on that date"""
    bm = booking_records.filter( day_of_the_week=day)
    cp_users = careplan_records.values_list('user__user_id', flat=True)
    bm_final = bm.filter(service_user__user_id__in=cp_users)
    return bm_final


def get_eligible_cw_on_day(cw_certificate , cw_employment):  ### HOW
    """takes cw skill certificate and cw employment info and date in period
    returns the cw who have valid contracts on that date """
    cw_final = cw_certificate.filter(user__user_id__in=cw_employment.values_list('user__user_id', flat=True))
    return cw_final


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
    alloc_qual = BookingAllocationQuality.objects.filter(booking__weekly_booking_id = bm.weekly_booking_id )
    if len(alloc_qual):
        alloc_qual = alloc_qual.exclude(Q(is_cw_hard_failed = True) | Q(is_su_hard_failed=True))
        cw_alloc_qual = alloc_qual.values_list('careworker', flat=True).distinct()
        cw_record = cw_record.filter(user__user_id__in = cw_alloc_qual)
    #
    else:
        # remove cw who do not fit into su's hard pref
        su_pref = HcmsSuPreference.objects.filter(user__user_id = bm.service_user.user_id , incorporation_type_mc_id = 662 )
        for su_record in su_pref:
            if su_record.preference_type_mc_id == 661:
                cw_record = cw_record.filter(user__profile__primary_language_mc_id = bm.service_user.profile.primary_language_mc_id)
            elif su_record.preference_type_mc_id == 660:
                cw_record = cw_record.filter(user__profile__ethnicity_mc_id=bm.service_user.profile.ethnicity_mc_id)
            elif su_record.preference_type_mc_id == 659:
                cw_record = cw_record.filter(user__profile__religion_mc_id=bm.service_user.profile.religion_mc_id)
            elif su_record.preference_type_mc_id == 657:
                cw_record = cw_record.filter(user__profile__sex_mc_id=bm.service_user.profile.sex_mc_id)
            elif su_record.preference_type_mc_id == 658:
                su_except = CWException.objects.filter(user__user_id = su_record.user.user_id ).values_list('exceptions')
                z = []
                if len(su_except)!=0:
                    y = [x for x in su_except][0][0].split(',')
                else:
                    y = []
                for w in y:
                    z.append(w)
                cw_record = cw_record.exclude(user__user_name__in = z)
        # remove cw who have hard pref conflicting with su
        cw_w_hard_pref = HcmsCwPreference.objects.filter(user__user_id__in= cw_record.values_list('user__user_id', flat=True))
        cw_w_hard_pref = cw_w_hard_pref.filter(incorporation_type_mc_id = 662)
        for cw_indiv in cw_w_hard_pref:
            if cw_indiv.preference_type_mc_id == 661 and cw_indiv.user.profile.primary_language_mc_id != bm.service_user.profile.primary_language_mc_id:
                cw_record = cw_record.exclude(user__user_id = cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 660 and cw_indiv.user.profile.ethnicity_mc_id != bm.service_user.profile.ethnicity_mc_id:
                cw_record = cw_record.exclude(user__user_id = cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 659 and cw_indiv.user.profile.religion_mc_id != bm.service_user.profile.religion_mc_id:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 657 and cw_indiv.user.profile.sex_mc_id != bm.service_user.profile.sex_mc_id:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 656 and bm.service_user.profile.is_non_smoker == 0:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 260 and bm.service_user.serviceuser.has_no_pets == 0:
                cw_record = cw_record.exclude(user__user_id=cw_indiv.user.user_id)
            elif cw_indiv.preference_type_mc_id == 665 and bm.booking_type_mc_id in [int(x) for x in cw_indiv.preference_value.split(',')]:
                cw_record = cw_record.exclude(user__user_id = cw_indiv.user.user_id)
    return cw_record


def get_cw_skill_dicts(cw_record):
    """takes the cw records valid on date as input
    gives output as two dictionaries, cw_skill_all and cw_skill fem
    which captures the skills and number of care workers for each for all cw and female cw
    dict format : {skill id: num of cw for skill, skill id: num of cw for skill , ...}"""
    cw_skill_all = {}
    cw_skill_fem = {}
    # get dictionary for all cw
    temp_cw_skill = cw_record.values_list('skills', flat=True)
    for skillset in temp_cw_skill:
        for indiv_skill in skillset:
            cw_skill_all[indiv_skill] = cw_skill_all.get(indiv_skill, 0) + 1
    # get cw for female cw
    temp_cw_skill = cw_record.filter(user__profile__sex_mc_id=8).values_list('skills', flat=True)
    for skillset in temp_cw_skill:
        for indiv_skill in skillset:
            cw_skill_fem[indiv_skill] = cw_skill_fem.get(indiv_skill, 0) + 1
    return cw_skill_all, cw_skill_fem


def update_solution_gender(sol, bm_day, slot, insuff, is_wom):
    """updates the insufficiency list when the insufficiency is detected
    returns the updated insufficiency list"""
    sol[bm_day]['insuff']['gender']['gen'].append((slot, insuff))
    if is_wom:
        sol[bm_day]['insuff']['gender']['fem'].append((slot, insuff))
    return sol


def update_solution_skill(sol, bm_day, slot, skill, insuff, is_wom):
    """updates the insufficiency list when the insufficiency is detected
    returns the updated insufficiency list"""
    sol[bm_day]['insuff']['skills'][skill] = sol[bm_day]['insuff']['skills'].get(skill, {'gen': [], 'fem':[]})
    sol[bm_day]['insuff']['skills'][skill]['gen'].append((slot, insuff))
    if is_wom:
        sol[bm_day]['insuff']['skills'][skill]['fem'].append((slot, insuff))
    return sol


def is_fine_tune_insuff(cw_cert_record, cw_employ_record, cw_slots, careplan, bm_record):
    """check whether there exist insufficiency in the period of consideration for valid bookings and care workers"""
    sol = get_sol_dict_template()
    # slot information
    slots = get_slots()
    # set ending of the bookings of h:00:00 to h-1:59:59 to make insufficiency calculation easier
    for bk in bm_record:
        if bk.end_time.minute == 00 and bk.end_time.second == 0:
            bk.end_time = time(bk.end_time.hour - 1,59,59)
    for cw in cw_slots:
        if cw.finished_time.minute == 00 and cw.finished_time.second == 0 :
            cw.finished_time = time((cw.finished_time.hour - 1)%24,59,59)
    for day in range(7):
        for slot in slots:
            cw_in_slot = cw_slots.exclude(Q(started_time__gt=slot[1]) | Q(finished_time__lt=slot[0]))
            cw_in_slot = cw_in_slot.filter(day_of_week = day)
            num_cw_in_slot = len(cw_in_slot.distinct('cw_availability__user__user_id'))
            sol[day]['cw avail']['gen'][slot[0].hour] = [slot[0].hour, num_cw_in_slot]
            sol[day]['cw avail']['fem'][slot[0].hour] = [slot[0].hour, len(cw_in_slot.filter(cw_availability__user__profile__sex_mc_id = 8).distinct('cw_availability__user__user_id'))]
        sol[day]['cw avail']['gen'].sort(key = lambda x:x[1])#key = lambda x:x[1]
        sol[day]['cw avail']['fem'].sort(key = lambda x:x[1])#key = lambda x:x[1]
    # iterate through all dates in the range to check insufficiency on each
    # careworkers valid
    cw_master = get_eligible_cw_on_day(cw_cert_record, cw_employ_record)
    for day in range(7):
        # bookings on the date
        bm_master = get_eligible_bookings_on_day(bm_record, careplan, day)
        # if no bookings on date go tio next date
        if len(bm_master) == 0:
            continue
        # for bookings on date
        for booking in bm_master:
            req_skill = booking.skills_required
            ###
            # get cw skill info dict, for all cw and female cw
            cw_skill_all, cw_skill_fem = get_cw_skill_dicts(cw_master)
            # check if su is a woman
            is_wom = bool(booking.service_user.profile.sex_mc_id == 8)
            # if the su is a woman, consider the other bookings having females, and only fem cw skills
            if is_wom:
                bm = bm_master.filter(service_user__profile__sex_mc_id=8)
                cw_skill = cw_skill_fem
            # else consider all bookings and cw
            else:
                bm = bm_master
                cw_skill = cw_skill_all
            # check if booking is overnight
            # hours = list of slots in which booking lies
            if booking.start_time > booking.end_time:
                hours = [tup for tup in slots if tup[0] < booking.end_time or tup[1] > booking.start_time]
                is_overnight = 1
            # hours = list of slots in which booking lies
            else:
                hours = [tup for tup in slots if not (tup[0] >= booking.end_time or tup[1] < booking.start_time)]
                is_overnight = 0
            # for slot in hours which booking is present
            for slot in hours:
                if is_overnight:
                    bm_slot = bm.filter(Q(start_time__gt = slot[1]) | Q(end_time__lt=slot[0]))
                else:
                    bm_slot = bm.exclude(Q(start_time__gt = slot[1]) | Q(end_time__lt = slot[0]))
                # get date of slot, i.e. next date of booking if the slot is the next morning of overnight booking
                if is_overnight and slot[1] < time(12, 0, 0):
                    bm_day_in_dict = (day+1)%7
                else:
                    bm_day_in_dict = day
                # total cw required in slot
                num_cw_req_in_slot = sum([x.no_of_cw for x in bm_slot])
                # total cw present in slot
                if is_wom:
                    total_cw_slot = sol[day]['cw avail']['fem'][slot[0].hour][1]
                else:
                    total_cw_slot = sol[day]['cw avail']['gen'][slot[0].hour][1]
                # if there is insufficiency in gender
                if num_cw_req_in_slot > total_cw_slot:
                    insuff_gender = num_cw_req_in_slot - total_cw_slot
                    sol = update_solution_gender(sol, bm_day_in_dict, slot, insuff_gender, is_wom)
                # for each skill in the required skills for booking
                for skill in req_skill:
                    # get num of cw with the skill
                    num_cw_w_skill = cw_skill.get(skill, 0)
                    # get total number of required care workers for the skill
                    num_req_cw_w_skill = sum([x.no_of_cw for x in bm_slot.filter(skills_required__contains=[skill])])
                    # if there is insufficiency, update the solution list
                    if num_req_cw_w_skill > num_cw_w_skill:
                        insuff_skill = num_req_cw_w_skill - num_cw_w_skill
                        sol = update_solution_skill(sol, bm_day_in_dict, slot, skill, insuff_skill, is_wom)
    # sort result by the num of insuff
    ##
    ##
    return sol


def continuous_slot(assignment):
    for day in assignment:
        slots = assignment[day]
        # if the slots are continuous join the slots
    return assignment


def get_new_cw_info():
    skill = [55, 76, 24]
    gender = 7
    cw = {'skills': skill, 'sex_id': gender}
    return cw


def get_assignment(new_cw, cw_cert, cwemploy, cw_slots, sucareplan, subooking):
    assignment = {0:[], 1:[],2:[],3:[],4:[],5:[],6:[]}
    insuff = is_fine_tune_insuff(cw_cert, cwemploy, cw_slots, sucareplan, subooking)
    #sol[bm_day]['insuff']['skills'][skill]['fem'].append((slot, insuff))
    if(new_cw['sex_id'] == 8):
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
                    assignment[day].append([(time(x[0], 0, 0) , time(x[0], 59, 59)) for x in insuff[day]['cw avail'][gender][0:5]])
    else:
        print('Enter the skills in care worker record')
    return assignment, insuff

# set start and end dates of the period of consideration
startdate, enddate = get_period_of_consideration()
# select the cw who have valid contracts in the period of consideration
cwemploy, cw_cert, cw_slots = cw_in_period(startdate, enddate)
# select valid bookings for the period of consideration
subooking, sucareplan = booking_in_period(startdate, enddate)
cw_info = get_new_cw_info()
new_cw_assignment, insuff = get_assignment ( cw_info, cw_cert, cwemploy, cw_slots, sucareplan, subooking)
for y in insuff:
    print(y)
    print(insuff[y]['cw avail'])
    print(insuff[y]['insuff'])
    print('----------')

print('Assignments: -----------')
for x in new_cw_assignment:
    print(x)
    print(new_cw_assignment[x])



