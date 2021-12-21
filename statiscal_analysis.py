'''
Gender Ratio (fem cw: fem su , gen cw:gen su)
Cw skill per skill - (req gen cw: present gen cw, req fem cw: present fem cw)
Availability for each cw - (nominal (contract hrs) : available (slot) hrs)
utilization for each cw - (nominal (contract) hrs) : utilized (allocated booking) hrs)
'''
from booking.models import ScheduledBooking , BookingAllocation# has duration, num cw , and su id
from cw.models import AvailabilitySlot , SkillTemplate , EmploymentRecord, Certificate
from su.models import SuWeeklyBooking
from django.db.models import Q, F
from django.utils import timezone
import datetime
#from datetime import time


def get_period_of_consideration():
    """ returns start date and end date to the period of consideration"""
    now = timezone.now()
    start = now.replace(day=21, month=8, year=2020)  # '2020-11-13 04:30:00'
    end = now.replace(day=start.day + 1, month=start.month, year=start.year)  # '2020-12-13 05:29:59'
    return start, end


def get_gen_fem_cw_inperiod (startdate, enddate):
    cwemploy = EmploymentRecord.objects.exclude(employment_contract_type_mc_id=1111)  ###
    cwemploy = cwemploy.exclude(Q(end_date__lt=startdate) | Q(start_date__gt=enddate))  ####
    cwemploy = cwemploy.filter(Q(terminated_on__gte=startdate) | Q(terminated_on__isnull=True))
    cwemploy = cwemploy.filter(employment_status=725)
    gen_cw = cwemploy.distinct()
    fem_cw = cwemploy.filter(user__profile__sex_mc_id = 8).distinct()
    return gen_cw, fem_cw


def get_req_gen_fem_cw_inperiod(startdate, enddate):
    valid_bookings = ScheduledBooking.objects.exclude(Q(finished_date_time__lt=startdate) | Q(started_date_time__gt=enddate))
    num_req_gen = sum(valid_bookings.values_list('no_of_cw', flat=True))
    num_req_fem = sum(valid_bookings.filter(service_user__profile__sex_mc_id = 8).values_list('no_of_cw', flat=True))
    return num_req_gen, num_req_fem


def get_slots_in_range(start_time, end_time, slot_time = 60):
    slots = []
    time1 = start_time.replace( minute=0, second= 0)
    time2 = time1.replace(hour=time1.hour, minute=59, second= 59)
    if end_time.minute == 00 and end_time.second == 00:
        end_time_res = end_time.replace(hour=end_time.hour - 1 , minute=59, second= 59)
    else:
        end_time_res = end_time.replace(hour=end_time.hour, minute=59, second=59)
    while time2 <= end_time_res:
        slots.append((time1, time2))
        time1 += datetime.timedelta(minutes=slot_time)
        time2 += datetime.timedelta(minutes=slot_time)
    return slots


#change format to dict
def gender_ratio (startdate, enddate):
    """takes the start and end date
    gives """
    sol = {}
    slots = get_slots_in_range(startdate, enddate)
    for (start , end) in slots:
        gen_cw , fem_cw = get_gen_fem_cw_inperiod (start, end)
        gen_cw = len(gen_cw.values_list('user_id',flat = True).distinct())
        fem_cw = len(fem_cw.values_list('user_id',flat = True).distinct())
        req_gen , req_fem = get_req_gen_fem_cw_inperiod(start, end)
        sol[(start.hour , end.hour +1 )] = {'gen': {'req': req_gen ,'avail': gen_cw } ,
                                         'fem': {'req': req_fem ,'avail': fem_cw } }
    return sol


def get_time_format(res , div):
    sol = {}
    for tup in res:
        tdelta = tup[2].seconds
        sol[tup[0]] = sol.get(tup[0] , {'nom': tup[1]*div , 'avail': 0})
        sol[tup[0]]['avail'] = sol[tup[0]]['avail'] + (tdelta / 3600 )
    return sol


#add in days/ (multiple days) parameters
def get_cw_nom_avail_hours(cw , days):
    cw_slots = AvailabilitySlot.objects.filter(
        cw_availability__user__user_id__in= cw.values_list('user__user_id', flat=True))
    for cw_indiv in cw_slots:
        if cw_indiv.finished_time.minute == 00 and cw_indiv.finished_time.second == 00:
            cw_indiv.finished_time = datetime.time((cw_indiv.finished_time.hour - 1) % 24, 59, 59)
            cw_indiv.save()
    res = cw_slots.filter(day_of_week__in = days).values_list('cw_availability__user__user_id', 'cw_availability__user__employment_record__availability_hr', F('finished_time') - F('started_time'))
    res = get_time_format(res , len(days)/7)
    return res


def ratio_available_hrs(start_date , end_date ,cw = None , days = None):
    if cw is None:
        cw, _ = get_gen_fem_cw_inperiod (start_date, end_date)# all cw in period
    if days is None:
        print('aaaaa')
        days = range(7)
    all_cw_nom_avail = get_cw_nom_avail_hours( cw , days)
    print(all_cw_nom_avail)


def get_time_format_util(nom, sched ):
    sol = {}
    for n in nom:
        sol[n[0]] = sol.get(n[0] , {'nom': n[1] , 'avail': 0})
        for s in sched:
            if (n[0] == s[0]):
                sol[n[0]]['avail'] = sol[n[0]]['avail'] + (s[1].seconds / 3600)
    return sol


def get_cw_nom_util_hours(startdate, enddate, cw):
    res1 = cw.values_list('user_id', 'availability_hr')
    valid_bm = BookingAllocation.objects.filter(
        booking__booking_status_mc_id= 749,
        booking__booking_allocation_result_mc_id= 747,
        booking__finished_date_time__gte= startdate,
        booking__started_date_time__lte= enddate,
        booking__delete_ind='N'
    )
    res2 = valid_bm.values_list('careworker', F('booking__finished_date_time') - F('booking__started_date_time') )
    res = get_time_format_util(res1, res2)
    return res


def ratio_utilized_hrs(start_date , end_date ,cw = None):
    if cw is None:
        cw, _ = get_gen_fem_cw_inperiod (start_date, end_date)# all cw in period
    all_cw_util_avail = get_cw_nom_util_hours(startdate, enddate , cw)
    print(all_cw_util_avail)


def get_gen_fem_cwskill_inperiod (start, end, skill):
    cwemploy = EmploymentRecord.objects.exclude(employment_contract_type_mc_id=1111)  ###
    cwemploy = cwemploy.exclude(Q(end_date__lte=start) | Q(start_date__gte=end))  ####
    cwemploy = cwemploy.filter(Q(terminated_on__gte=start) | Q(terminated_on__isnull=True))
    cwemploy = cwemploy.filter(employment_status=725)
    cwcert =  Certificate.objects.filter(skills__contains=[skill]) #.exclude(Q(valid_from__gte =  enddate)| Q(valid_to__lte =  startdate))
    cwemploy = cwemploy.filter(user__user_id__in = cwcert.values_list('user__user_id', flat=True))
    gen_cw = cwemploy.distinct()
    fem_cw = cwemploy.filter(user__profile__sex_mc_id = 8).distinct()
    return gen_cw, fem_cw


def get_req_gen_fem_cwskill_inperiod(start, end ,skill):
    valid_bm = BookingAllocation.objects.filter(
        booking__booking_status_mc_id= 749,
        booking__booking_allocation_result_mc_id= 747,
        booking__delete_ind='N')
    valid_bm = valid_bm.exclude(Q(booking__finished_date_time__lt=start) | Q(booking__started_date_time__gt=end))
    weekly_bm = SuWeeklyBooking.objects.filter( skills_required__contains = [skill] )
    valid_bookings = valid_bm.filter( booking__weekly_booking_id__in = weekly_bm.values_list('weekly_booking_id', flat=True))
    num_req_gen = sum(valid_bookings.values_list('booking__no_of_cw', flat=True))
    num_req_fem = sum(valid_bookings.filter(booking__service_user__profile__sex_mc_id = 8).values_list('booking__no_of_cw', flat=True))
    return num_req_gen, num_req_fem


def get_all_skill():
    all_skill = SkillTemplate.objects.values_list('skill_template_id', flat=True)
    return all_skill


def skill_ratio (startdate, enddate):
    """takes the start and end date
    gives """
    sol = {}
    slots = get_slots_in_range(startdate, enddate)
    all_skills = get_all_skill()
    for (start , end) in slots:
            for skill in all_skills:
                gen_cw , fem_cw = get_gen_fem_cwskill_inperiod (start, end, skill)
                gen_cw = len(gen_cw.values_list('user_id',flat = True).distinct())
                fem_cw = len(fem_cw.values_list('user_id',flat = True).distinct())
                req_gen , req_fem = get_req_gen_fem_cwskill_inperiod(start, end ,skill)
                sol[(start.hour, end.hour + 1)] = sol.get((start.hour , end.hour +1 ) , {})
                sol[(start.hour , end.hour +1 )][skill] = sol[(start.hour , end.hour +1 )].get(skill , [])
                sol[(start.hour , end.hour +1 )][skill].append({'gen': {'req': req_gen ,'avail': gen_cw } ,
                                         'fem': {'req': req_fem ,'avail': fem_cw } })
    return sol


startdate, enddate = get_period_of_consideration()

#ratio_available_hrs(startdate , enddate , cw = None , days = [0])
#ratio_utilized_hrs(startdate , enddate , cw = None)

#print('start time: ', startdate , ' \n end time : ', enddate)
#slots = get_slots_in_range(startdate,enddate, 60)
#for sl in slots:
#    print(sl)
#ratio = gender_ratio(startdate, enddate)
ratio = skill_ratio(startdate, enddate)
for i in ratio:
    print( i )
    print(ratio[i])


print([x for x in ratio[(12, 13)] if ratio[(12,13)][x][0]['gen']['req'] != 0])
#print(ratio[(12,13)])






