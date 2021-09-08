# EXCLUDE RATHER THEN INCLUDE FOR SELECTION

#imports
from cw.models import EmploymentRecord
from su.models import SuWeeklyBooking
from django.db.models import Q
from django.utils import timezone

def get_cw_per_skill(cw_record):
    # inputs: careworker record, returns: dict with no of careworkers for each skill (both all and women)
    cwdict = {'all': {}, 'fem': {}}
    for x in cw_record:
        for s in x.user.cw_skill.first().skills:
            cwdict['all'][s] = cwdict['all'].get(s, 0) + 1
            if x.user.profile.sex_mc_id == 8:
                cwdict['fem'][s] = cwdict['fem'].get(s, 0) + 1
    return cwdict

def get_skills_for_bookings( bookings):
    #inputs: booking record,
    #returns: dict with bookings {all:{day:{hour:{skill:{num cw required with skill}}}}, fem:{day:{hour:{skill:{num cw required with skill}}}}}
    bookings_dict = {
        0: {0: {'all': {}, 'fem': {}}, 1: {'all': {}, 'fem': {}}, 2: {'all': {}, 'fem': {}}, 3: {'all': {}, 'fem': {}},
            4: {'all': {}, 'fem': {}}, 5: {'all': {}, 'fem': {}}, 6: {'all': {}, 'fem': {}}, 7: {'all': {}, 'fem': {}},
            8: {'all': {}, 'fem': {}}, 9: {'all': {}, 'fem': {}}, 10: {'all': {}, 'fem': {}},
            11: {'all': {}, 'fem': {}},
            12: {'all': {}, 'fem': {}}, 13: {'all': {}, 'fem': {}}, 14: {'all': {}, 'fem': {}},
            15: {'all': {}, 'fem': {}},
            16: {'all': {}, 'fem': {}}, 17: {'all': {}, 'fem': {}}, 18: {'all': {}, 'fem': {}},
            19: {'all': {}, 'fem': {}},
            20: {'all': {}, 'fem': {}}, 21: {'all': {}, 'fem': {}}, 22: {'all': {}, 'fem': {}},
            23: {'all': {}, 'fem': {}}},
        1: {0: {'all': {}, 'fem': {}}, 1: {'all': {}, 'fem': {}}, 2: {'all': {}, 'fem': {}}, 3: {'all': {}, 'fem': {}},
            4: {'all': {}, 'fem': {}}, 5: {'all': {}, 'fem': {}}, 6: {'all': {}, 'fem': {}}, 7: {'all': {}, 'fem': {}},
            8: {'all': {}, 'fem': {}}, 9: {'all': {}, 'fem': {}}, 10: {'all': {}, 'fem': {}},
            11: {'all': {}, 'fem': {}},
            12: {'all': {}, 'fem': {}}, 13: {'all': {}, 'fem': {}}, 14: {'all': {}, 'fem': {}},
            15: {'all': {}, 'fem': {}},
            16: {'all': {}, 'fem': {}}, 17: {'all': {}, 'fem': {}}, 18: {'all': {}, 'fem': {}},
            19: {'all': {}, 'fem': {}},
            20: {'all': {}, 'fem': {}}, 21: {'all': {}, 'fem': {}}, 22: {'all': {}, 'fem': {}},
            23: {'all': {}, 'fem': {}}},
        2: {0: {'all': {}, 'fem': {}}, 1: {'all': {}, 'fem': {}}, 2: {'all': {}, 'fem': {}}, 3: {'all': {}, 'fem': {}},
            4: {'all': {}, 'fem': {}}, 5: {'all': {}, 'fem': {}}, 6: {'all': {}, 'fem': {}}, 7: {'all': {}, 'fem': {}},
            8: {'all': {}, 'fem': {}}, 9: {'all': {}, 'fem': {}}, 10: {'all': {}, 'fem': {}},
            11: {'all': {}, 'fem': {}},
            12: {'all': {}, 'fem': {}}, 13: {'all': {}, 'fem': {}}, 14: {'all': {}, 'fem': {}},
            15: {'all': {}, 'fem': {}},
            16: {'all': {}, 'fem': {}}, 17: {'all': {}, 'fem': {}}, 18: {'all': {}, 'fem': {}},
            19: {'all': {}, 'fem': {}},
            20: {'all': {}, 'fem': {}}, 21: {'all': {}, 'fem': {}}, 22: {'all': {}, 'fem': {}},
            23: {'all': {}, 'fem': {}}},
        3: {0: {'all': {}, 'fem': {}}, 1: {'all': {}, 'fem': {}}, 2: {'all': {}, 'fem': {}}, 3: {'all': {}, 'fem': {}},
            4: {'all': {}, 'fem': {}}, 5: {'all': {}, 'fem': {}}, 6: {'all': {}, 'fem': {}}, 7: {'all': {}, 'fem': {}},
            8: {'all': {}, 'fem': {}}, 9: {'all': {}, 'fem': {}}, 10: {'all': {}, 'fem': {}},
            11: {'all': {}, 'fem': {}},
            12: {'all': {}, 'fem': {}}, 13: {'all': {}, 'fem': {}}, 14: {'all': {}, 'fem': {}},
            15: {'all': {}, 'fem': {}},
            16: {'all': {}, 'fem': {}}, 17: {'all': {}, 'fem': {}}, 18: {'all': {}, 'fem': {}},
            19: {'all': {}, 'fem': {}},
            20: {'all': {}, 'fem': {}}, 21: {'all': {}, 'fem': {}}, 22: {'all': {}, 'fem': {}},
            23: {'all': {}, 'fem': {}}},
        4: {0: {'all': {}, 'fem': {}}, 1: {'all': {}, 'fem': {}}, 2: {'all': {}, 'fem': {}}, 3: {'all': {}, 'fem': {}},
            4: {'all': {}, 'fem': {}}, 5: {'all': {}, 'fem': {}}, 6: {'all': {}, 'fem': {}}, 7: {'all': {}, 'fem': {}},
            8: {'all': {}, 'fem': {}}, 9: {'all': {}, 'fem': {}}, 10: {'all': {}, 'fem': {}},
            11: {'all': {}, 'fem': {}},
            12: {'all': {}, 'fem': {}}, 13: {'all': {}, 'fem': {}}, 14: {'all': {}, 'fem': {}},
            15: {'all': {}, 'fem': {}},
            16: {'all': {}, 'fem': {}}, 17: {'all': {}, 'fem': {}}, 18: {'all': {}, 'fem': {}},
            19: {'all': {}, 'fem': {}},
            20: {'all': {}, 'fem': {}}, 21: {'all': {}, 'fem': {}}, 22: {'all': {}, 'fem': {}},
            23: {'all': {}, 'fem': {}}},
        5: {0: {'all': {}, 'fem': {}}, 1: {'all': {}, 'fem': {}}, 2: {'all': {}, 'fem': {}}, 3: {'all': {}, 'fem': {}},
            4: {'all': {}, 'fem': {}}, 5: {'all': {}, 'fem': {}}, 6: {'all': {}, 'fem': {}}, 7: {'all': {}, 'fem': {}},
            8: {'all': {}, 'fem': {}}, 9: {'all': {}, 'fem': {}}, 10: {'all': {}, 'fem': {}},
            11: {'all': {}, 'fem': {}},
            12: {'all': {}, 'fem': {}}, 13: {'all': {}, 'fem': {}}, 14: {'all': {}, 'fem': {}},
            15: {'all': {}, 'fem': {}},
            16: {'all': {}, 'fem': {}}, 17: {'all': {}, 'fem': {}}, 18: {'all': {}, 'fem': {}},
            19: {'all': {}, 'fem': {}},
            20: {'all': {}, 'fem': {}}, 21: {'all': {}, 'fem': {}}, 22: {'all': {}, 'fem': {}},
            23: {'all': {}, 'fem': {}}},
        6: {0: {'all': {}, 'fem': {}}, 1: {'all': {}, 'fem': {}}, 2: {'all': {}, 'fem': {}}, 3: {'all': {}, 'fem': {}},
            4: {'all': {}, 'fem': {}}, 5: {'all': {}, 'fem': {}}, 6: {'all': {}, 'fem': {}}, 7: {'all': {}, 'fem': {}},
            8: {'all': {}, 'fem': {}}, 9: {'all': {}, 'fem': {}}, 10: {'all': {}, 'fem': {}},
            11: {'all': {}, 'fem': {}},
            12: {'all': {}, 'fem': {}}, 13: {'all': {}, 'fem': {}}, 14: {'all': {}, 'fem': {}},
            15: {'all': {}, 'fem': {}},
            16: {'all': {}, 'fem': {}}, 17: {'all': {}, 'fem': {}}, 18: {'all': {}, 'fem': {}},
            19: {'all': {}, 'fem': {}},
            20: {'all': {}, 'fem': {}}, 21: {'all': {}, 'fem': {}}, 22: {'all': {}, 'fem': {}},
            23: {'all': {}, 'fem': {}}}
    }
    for booking in bookings:
        day = booking.day_of_the_week
        st_hr = booking.start_time.hour
        end_hr = booking.end_time.hour
        num_cw = booking.no_of_cw
        skill_req = booking.skills_required
        for h in range(st_hr, end_hr + 1):
            for s in skill_req:
                bookings_dict[day][h]['all'][s] = bookings_dict[day][h]['all'].get(s, 0) + num_cw
                if booking.service_user.profile.sex_mc_id == 8:
                    bookings_dict[day][h]['fem'][s] = bookings_dict[day][h]['fem'].get(s, 0) + num_cw
    print(bookings_dict)
    return bookings_dict

def test_sufficiency (cw_dict , bm_dict):
    insuff = {'all': [], 'fem': []}
    cwskills_all = list(cw_dict['all'].keys())
    cwskills_fem = list(cw_dict['fem'].keys())
    for day in bm_dict:
        for h in bm_dict[day]:
            for skill in bm_dict[day][h]['all']:
                if skill not in cwskills_all:
                    print('No cw for day ', day, ' hour ', h, ' skill ', skill)
                elif (cw_dict['all'][skill] >= bm_dict[day][h]['all'][skill]):
                    continue
                insuff['all'].append((day, h, skill, bm_dict[day][h]['all'][skill] - cw_dict['all'].get(skill, 0)))
            for skill in bm_dict[day][h]['fem']:
                if skill not in cwskills_all:
                    print('No female cw for day ', day, ' hour ', h, ' skill ', skill)
                elif (cw_dict['fem'][skill] >= bm_dict[day][h]['fem'][skill]):
                    continue
                insuff['fem'].append((day, h, skill, bm_dict[day][h]['fem'][skill] - cw_dict['fem'].get(skill, 0)))
    return(insuff)


# get UTC timezone date time for required period
now = timezone.now()
startdate = now.replace(day = 13, month = 11, year = 2020 ) #'2020-11-13'
enddate = now.replace(day = 13, month = 12, year = 2020 )# '2020-12-13'

#get records of cw who have valid contracts for time between start and end date
cwemploy = EmploymentRecord.objects.filter( employment_status = 725 )
cwemploy = cwemploy.filter(Q( terminated_on__gte = enddate) | Q( terminated_on__isnull = True))
cwemploy = cwemploy.exclude(employment_contract_type_mc_id = 1111,  end_date__lt = startdate,  start_date__gt = enddate  )
cwemploy = cwemploy.exclude( Q(user__cw_skill__valid_from__gte = enddate)| Q( user__cw_skill__valid_to__lte = startdate))
#get no of careworkers for each skill (both all and women)
#cw_dict = {'all':{skill: no of all cw with that skill}, 'fem':{skill: no of female cw with that skill}}
cw_dict = get_cw_per_skill( cwemploy)
print(cw_dict)

#get bookings info for valid bookings made by valid users between period
subooking = SuWeeklyBooking.objects.exclude(valid_to__lt = startdate , valid_from__gt = enddate)
subooking = subooking.exclude( Q(service_user__care_plan__start_date__gt = enddate) | Q( service_user__care_plan__end_date__lt = startdate ))
#subooking = subooking.filter(Q(service_user__care_plan__termination_date__gte = enddate) | Q(service_user__care_plan__termination_date__isnull = True))
subooking = subooking.exclude(Q(service_user__care_plan__termination_date__lte = startdate))

#get skills required for bookings for each hour of the day
bm_dict = get_skills_for_bookings( subooking)

## test
if_suff = test_sufficiency(cw_dict , bm_dict )
#if_suff is dict with keys all and fem
#if_suff['all'] empty if no insufficiency in all cw, else has a list of tuples (day, hour,skill, num of cw shortage)
if(len(if_suff['all'])):
    print('Insufficient cw for all genders ', if_suff['all'])
else:
    print('For all genders data is sufficient')

#if_suff['fem'] empty if no insufficiency in fem cw, else has a list of tuples (day, hour,skill, num of cw shortage)
if(len(if_suff['fem'])):
    print('Insufficient cw for women ', if_suff['fem'])
else:
    print('For women data is sufficient')


print(cw_dict)


