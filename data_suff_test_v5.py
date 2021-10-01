#dict (with query set)
#with required format
#
#imports
from cw.models import EmploymentRecord
from cw.models import Certificate
from su.models import SuWeeklyBooking
from su.models import CarePlan
from django.db.models import Q
from pandas import date_range
from django.utils import timezone
from datetime import time, timedelta


def get_period_of_consideration():
    """ returns start date and end date to the period of consideration """
    now = timezone.now()
    start = now.replace(day=13, month=11, year=2020)  # '2020-11-13 04:30:00'
    end = now.replace(day=13, month=12, year=2020)  # '2020-12-13 05:29:59'
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
    return cwemploy, cw_cert


def booking_in_period(startdate, enddate):
    """takes the start and end date of the period as input
    gives booking info (booking details and care plan details) for valid bookings and care plans in the period"""
    subooking = SuWeeklyBooking.objects.exclude(Q(valid_to__lt=startdate) | Q(valid_from__gt=enddate))
    sucareplan = CarePlan.objects.exclude(termination_date__lte=startdate)
    sucareplan = sucareplan.exclude(Q(end_date__lt=startdate) | Q(start_date__gt=enddate))
    return subooking, sucareplan


def get_eligible_bookings_on_date(booking_records, careplan_records, date):
    """takes booking and care plan info and date in period
    returns the bookings which exist on that date"""
    bm = booking_records.filter(valid_to__gte=date, day_of_the_week=date.dayofweek, valid_from__lte=date)
    cp = careplan_records.filter(start_date__lte=date, end_date__gte=date)
    cp = cp.filter(Q(termination_date__gt=date) | Q(termination_date__isnull=True))
    cp_users = cp.values_list('user__user_id', flat=True)
    bm_final = bm.filter(service_user__user_id__in=cp_users)
    return bm_final


def get_eligible_cw_on_date(cw_certificate , cw_employment, date):
    """takes cw skill certificate and cw employment info and date in period
    returns the cw who have valid contracts on that date """
    cw_certificate = cw_certificate.filter(valid_to__gte=date, valid_from__lte=date)
    cw_emp = cw_employment.filter(Q(terminated_on__gt=date) | Q(terminated_on__isnull=True))
    cw_emp = cw_emp.filter(start_date__lte=date, end_date__gte=date)
    cw_final = cw_certificate.filter(user__user_id__in=cw_emp.values_list('user__user_id', flat=True))
    return cw_final


def get_slots():
    """returns a list of tuples where each tuple has the start time of the slot
    and the end time of the slot (inclusive)"""
    slots = [(time(0, 0, 0), time(0, 59, 59)), (time(1, 0, 0), time(1, 59, 59)), (time(2, 0, 0), time(2, 59, 59)),
             (time(3, 0, 0), time(3, 59, 59)), (time(4, 0, 0), time(4, 59, 59)), (time(5, 0, 0), time(6, 59, 59)),
             (time(7, 0, 0), time(7, 59, 59)), (time(8, 0, 0), time(8, 59, 59)), (time(9, 0, 0), time(9, 59, 59)),
             (time(10, 0, 0), time(10, 59, 59)), (time(11, 0, 0), time(11, 59, 59)), (time(12, 0, 0), time(12, 59, 59)),
             (time(13, 0, 0), time(13, 59, 59)), (time(14, 0, 0), time(14, 59, 59)), (time(15, 0, 0), time(15, 59, 59)),
             (time(16, 0, 0), time(16, 59, 59)), (time(17, 0, 0), time(17, 59, 59)), (time(18, 0, 0), time(18, 59, 59)),
             (time(19, 0, 0), time(19, 59, 59)), (time(20, 0, 0), time(20, 59, 59)), (time(21, 0, 0), time(21, 59, 59)),
             (time(22, 0, 0), time(22, 59, 59)), (time(23, 0, 0), time(23, 59, 59))]
    return slots


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


def update_solution(sol, bm_date, slot, skill, insuff, is_wom):
    """updates the insufficiency list when the insufficiency is detected
    returns the updated insufficiency list"""
    # get index of the dict for the date having insufficiency if present
    # if not then append the date with corresponding slot, skill, and set insufficiency to 0
    # set index to that of the last element
    try:
        i = [x['date'] == bm_date for x in sol if len(sol)].index(True)
    except:
        i = len(sol)
        sol.append({'date': bm_date, 'slot_details': [
            {'slot_time_start': slot[0], 'slot_time_end': slot[1],
             'insufficiency': [{'skill_id': skill, 'female_skill_insufficiency': 0,
                                'overall_skill_insufficiency': 0}]}]})
    # get index of the dict for the slot time in the date having insufficiency if present
    # if not then append the slot with corresponding  skill, set insufficiency to 0
    # set index to that of the last element
    try:
        j = [x['slot_time_start'] == slot[0] for x in sol[i]['slot_details'] if
             len(sol[i]['slot_details'])].index(1)
    except:
        j = len(sol[i]['slot_details'])
        sol[i]['slot_details'].append({'slot_time_start': slot[0], 'slot_time_end': slot[1],
                                       'insufficiency': [
                                           {'skill_id': skill, 'female_skill_insufficiency': 0,
                                            'overall_skill_insufficiency': 0}]})
    # get index of the dict for the skill id in the slot and date having insufficiency if present
    # if not then append the skill with corresponding  and set insufficiency to 0
    # set index to that of the last element
    try:
        k = [x['skill_id'] == skill for x in sol[i]['slot_details'][j]['insufficiency'] if
             len(sol[i]['slot_details'][j]['insufficiency'])].index(1)
    except:
        k = len(sol[i]['slot_details'][j]['insufficiency'])
        sol[i]['slot_details'][j]['insufficiency'].append(
            {'skill_id': skill, 'female_skill_insufficiency': 0,
             'overall_skill_insufficiency': 0})
    # set insufficiency as max calculated insufficiency and if woman su, add woman insufficiency
    sol[i]['slot_details'][j]['insufficiency'][k]['overall_skill_insufficiency'] = max(
        sol[i]['slot_details'][j]['insufficiency'][k]['overall_skill_insufficiency'],
        insuff)
    if is_wom:
        sol[i]['slot_details'][j]['insufficiency'][k]['female_skill_insufficiency'] = max(
            sol[i]['slot_details'][j]['insufficiency'][k]['female_skill_insufficiency'],
            insuff)
    return sol


def is_insuff(cw_cert_record, cw_employ_record, careplan, bm_record, startdate, enddate):
    """check whether there exist insufficiency in the period of consideration for valid bookings and care workers"""
    sol = []
    # get all the dates in range
    dates_in_range = date_range(start=startdate, end=enddate)
    # set ending of the bookings of h:00:00 to h-1:59:59 to make insufficiency calculation easier
    for bk in bm_record:
        if bk.end_time.minute == 00 and bk.end_time.second == 0:
            bk.end_time =  time(bk.end_time.hour - 1,59,59)
    # iterate through all dates in the range to check insufficiency on each
    for date in dates_in_range:
        # bookings on the date
        bm_master = get_eligible_bookings_on_date(bm_record, careplan, date)
        # if no bookings on date go tio next date
        if len(bm_master) == 0:
            continue
        # careworkers valid on the given date
        cw_master = get_eligible_cw_on_date(cw_cert_record, cw_employ_record, date)
        # slot information
        slots = get_slots()
        # get cw skill info dict, for all cw and female cw
        cw_skill_all, cw_skill_fem = get_cw_skill_dicts(cw_master)
        # for bookings on date
        for booking in bm_master:
            req_skill = booking.skills_required
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
                # get other bookings also valid in slot
                if is_overnight:
                    bm_slot = bm.filter(Q(start_time__gt = slot[1]) | Q(end_time__lt=slot[0]))
                else:
                    bm_slot = bm.exclude(Q(start_time__gt = slot[1]) | Q(end_time__lt = slot[0]))
                # get date of slot, i.e. next date of booking if the slot is the next morning of overnight booking
                if is_overnight and slot[1] < time(12, 0, 0):
                    bm_date_in_dict = date.date() + timedelta(days=1)
                else:
                    bm_date_in_dict = date.date()
                # for each skill in the required skills for booking
                for skill in req_skill:
                    # get num of cw with the skill
                    num_cw_w_skill = cw_skill.get(skill, 0)
                    # get total number of required care workers for the skill
                    num_req_cw_w_skill = sum([x.no_of_cw for x in bm_slot.filter(skills_required__contains=[skill])])
                    # if there is insufficiency, update the solution list
                    if num_req_cw_w_skill > num_cw_w_skill:
                        insuff_skill = num_req_cw_w_skill - num_cw_w_skill
                        sol = update_solution(sol, bm_date_in_dict, slot, skill, insuff_skill, is_wom)
    # sort result by the date of insufficiency
    sol.sort(key=lambda x: x['date'])
    return sol


def main():
    # set start and end dates of the period of consideration
    startdate, enddate = get_period_of_consideration()
    # select the cw who have valid contracts in the period of consideration
    cwemploy, cw_cert = cw_in_period(startdate, enddate)
    # select valid bookings for the period of consideration
    subooking, sucareplan = booking_in_period(startdate, enddate)
    # calculate the insufficiency for the given period of consideration
    insuff_skill_indiv = is_insuff(cw_cert, cwemploy, sucareplan, subooking, startdate, enddate)
    # print insufficiency
    for x in insuff_skill_indiv:
        print(x)


main()





