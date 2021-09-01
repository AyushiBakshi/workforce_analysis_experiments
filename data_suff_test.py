from cw.models import EmploymentRecord
from su.models import SuWeeklyBooking
from django.db.models import Q

from django.utils import timezone
now = timezone.now()

startdate = now.replace(day = 13, month = 11, year = 2020 ) #'2020-11-13 04:30:00'
enddate = now.replace(day = 13, month = 12, year = 2020 )# '2020-12-13 05:29:59'

cwemploy = EmploymentRecord.objects.filter( employment_status = 725 , start_date__lte = startdate,  end_date__gte = enddate  ).filter(Q( terminated_on__gte = enddate) | Q( terminated_on__isnull = True)).exclude(employment_contract_type_mc_id = 1111).filter(user__cw_skill__valid_from__lte = startdate, user__cw_skill__valid_to__gte = enddate)
cw_dict = {'all':{}, 'fem':{}}

for x in cwemploy:
    for s in x.user.cw_skill.first().skills:
        cw_dict['all'][s] = cw_dict['all'].get(s, 0) + 1
        if x.user.profile.sex_mc_id == 8:
            cw_dict['fem'][s] = cw_dict['fem'].get(s, 0) + 1

print(cw_dict)

bm_dict = {0:{0:{'all':{},'fem':{}}, 1:{'all':{},'fem':{}},2:{'all':{},'fem':{}},3:{'all':{},'fem':{}},
              4:{'all':{},'fem':{}},5:{'all':{},'fem':{}},6:{'all':{},'fem':{}},7:{'all':{},'fem':{}},
              8:{'all':{},'fem':{}},9:{'all':{},'fem':{}},10:{'all':{},'fem':{}},11:{'all':{},'fem':{}},
              12:{'all':{},'fem':{}},13:{'all':{},'fem':{}},14:{'all':{},'fem':{}},15:{'all':{},'fem':{}},
              16:{'all':{},'fem':{}},17:{'all':{},'fem':{}},18:{'all':{},'fem':{}},19:{'all':{},'fem':{}},
              20:{'all':{},'fem':{}},21:{'all':{},'fem':{}},22:{'all':{},'fem':{}},23:{'all':{},'fem':{}}},
           1:{0:{'all':{},'fem':{}}, 1:{'all':{},'fem':{}},2:{'all':{},'fem':{}},3:{'all':{},'fem':{}},
              4:{'all':{},'fem':{}},5:{'all':{},'fem':{}},6:{'all':{},'fem':{}},7:{'all':{},'fem':{}},
              8:{'all':{},'fem':{}},9:{'all':{},'fem':{}},10:{'all':{},'fem':{}},11:{'all':{},'fem':{}},
              12:{'all':{},'fem':{}},13:{'all':{},'fem':{}},14:{'all':{},'fem':{}},15:{'all':{},'fem':{}},
              16:{'all':{},'fem':{}},17:{'all':{},'fem':{}},18:{'all':{},'fem':{}},19:{'all':{},'fem':{}},
              20:{'all':{},'fem':{}},21:{'all':{},'fem':{}},22:{'all':{},'fem':{}},23:{'all':{},'fem':{}}},
           2:{0:{'all':{},'fem':{}}, 1:{'all':{},'fem':{}},2:{'all':{},'fem':{}},3:{'all':{},'fem':{}},
              4:{'all':{},'fem':{}},5:{'all':{},'fem':{}},6:{'all':{},'fem':{}},7:{'all':{},'fem':{}},
              8:{'all':{},'fem':{}},9:{'all':{},'fem':{}},10:{'all':{},'fem':{}},11:{'all':{},'fem':{}},
              12:{'all':{},'fem':{}},13:{'all':{},'fem':{}},14:{'all':{},'fem':{}},15:{'all':{},'fem':{}},
              16:{'all':{},'fem':{}},17:{'all':{},'fem':{}},18:{'all':{},'fem':{}},19:{'all':{},'fem':{}},
              20:{'all':{},'fem':{}},21:{'all':{},'fem':{}},22:{'all':{},'fem':{}},23:{'all':{},'fem':{}}},
           3:{0:{'all':{},'fem':{}}, 1:{'all':{},'fem':{}},2:{'all':{},'fem':{}},3:{'all':{},'fem':{}},
              4:{'all':{},'fem':{}},5:{'all':{},'fem':{}},6:{'all':{},'fem':{}},7:{'all':{},'fem':{}},
              8:{'all':{},'fem':{}},9:{'all':{},'fem':{}},10:{'all':{},'fem':{}},11:{'all':{},'fem':{}},
              12:{'all':{},'fem':{}},13:{'all':{},'fem':{}},14:{'all':{},'fem':{}},15:{'all':{},'fem':{}},
              16:{'all':{},'fem':{}},17:{'all':{},'fem':{}},18:{'all':{},'fem':{}},19:{'all':{},'fem':{}},
              20:{'all':{},'fem':{}},21:{'all':{},'fem':{}},22:{'all':{},'fem':{}},23:{'all':{},'fem':{}}},
           4:{0:{'all':{},'fem':{}}, 1:{'all':{},'fem':{}},2:{'all':{},'fem':{}},3:{'all':{},'fem':{}},
              4:{'all':{},'fem':{}},5:{'all':{},'fem':{}},6:{'all':{},'fem':{}},7:{'all':{},'fem':{}},
              8:{'all':{},'fem':{}},9:{'all':{},'fem':{}},10:{'all':{},'fem':{}},11:{'all':{},'fem':{}},
              12:{'all':{},'fem':{}},13:{'all':{},'fem':{}},14:{'all':{},'fem':{}},15:{'all':{},'fem':{}},
              16:{'all':{},'fem':{}},17:{'all':{},'fem':{}},18:{'all':{},'fem':{}},19:{'all':{},'fem':{}},
              20:{'all':{},'fem':{}},21:{'all':{},'fem':{}},22:{'all':{},'fem':{}},23:{'all':{},'fem':{}}},
           5:{0:{'all':{},'fem':{}}, 1:{'all':{},'fem':{}},2:{'all':{},'fem':{}},3:{'all':{},'fem':{}},
              4:{'all':{},'fem':{}},5:{'all':{},'fem':{}},6:{'all':{},'fem':{}},7:{'all':{},'fem':{}},
              8:{'all':{},'fem':{}},9:{'all':{},'fem':{}},10:{'all':{},'fem':{}},11:{'all':{},'fem':{}},
              12:{'all':{},'fem':{}},13:{'all':{},'fem':{}},14:{'all':{},'fem':{}},15:{'all':{},'fem':{}},
              16:{'all':{},'fem':{}},17:{'all':{},'fem':{}},18:{'all':{},'fem':{}},19:{'all':{},'fem':{}},
              20:{'all':{},'fem':{}},21:{'all':{},'fem':{}},22:{'all':{},'fem':{}},23:{'all':{},'fem':{}}},
           6:{0:{'all':{},'fem':{}}, 1:{'all':{},'fem':{}},2:{'all':{},'fem':{}},3:{'all':{},'fem':{}},
              4:{'all':{},'fem':{}},5:{'all':{},'fem':{}},6:{'all':{},'fem':{}},7:{'all':{},'fem':{}},
              8:{'all':{},'fem':{}},9:{'all':{},'fem':{}},10:{'all':{},'fem':{}},11:{'all':{},'fem':{}},
              12:{'all':{},'fem':{}},13:{'all':{},'fem':{}},14:{'all':{},'fem':{}},15:{'all':{},'fem':{}},
              16:{'all':{},'fem':{}},17:{'all':{},'fem':{}},18:{'all':{},'fem':{}},19:{'all':{},'fem':{}},
              20:{'all':{},'fem':{}},21:{'all':{},'fem':{}},22:{'all':{},'fem':{}},23:{'all':{},'fem':{}}}}


subooking = SuWeeklyBooking.objects.filter(valid_from__lte = startdate , valid_to__gte = enddate).filter(service_user__care_plan__start_date__lte = startdate, service_user__care_plan__end_date__gte = enddate ).filter(Q( service_user__care_plan__termination_date__gte = enddate) | Q( service_user__care_plan__termination_date__isnull = True))

for x in subooking:
    day = x.day_of_the_week
    st_hr = x.start_time.hour
    end_hr = x.end_time.hour
    num_cw = x.no_of_cw
    skill_req = x.skills_required
    for h in range(st_hr, end_hr+1):
        for s in skill_req:
            bm_dict[day][h]['all'][s] = bm_dict[day][h]['all'].get(s,0) + num_cw
        if x.service_user.profile.sex_mc_id == 8:
            bm_dict[day][h]['fem'][s] = bm_dict[day][h]['fem'].get(s, 0) + num_cw

print(bm_dict)



## test
insuff = {'all':[], 'fem':[]}
cwskills_all = list(cw_dict['all'].keys())
cwskills_fem = list(cw_dict['fem'].keys())
for day in bm_dict:
    for h in bm_dict[day]:
        for skill in bm_dict[day][h]['all']:
            if skill not in cwskills_all:
                print('No cw for day ', day, ' hour ', h, ' skill ', skill)
            elif ( cw_dict['all'][skill] >= bm_dict[day][h]['all'][skill]) :
                continue
            insuff['all'].append((day, h, skill, bm_dict[day][h]['all'][skill] - cw_dict['all'].get(skill, 0)))
        for skill in bm_dict[day][h]['fem']:
            if skill not in cwskills_all:
                print('No female cw for day ', day, ' hour ', h, ' skill ', skill)
            elif ( cw_dict['fem'][skill] >= bm_dict[day][h]['fem'][skill]):
                continue
            insuff['fem'].append((day, h, skill, bm_dict[day][h]['fem'][skill] - cw_dict['fem'].get(skill, 0)))



if(len(insuff['all'])):
    print('Insufficient cw for all genders ', insuff['all'])
else:
    print('For all genders data is sufficient')

if(len(insuff['fem'])):
    print('Insufficient cw for women ', insuff['fem'])
else:
    print('For women data is sufficient')




