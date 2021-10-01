#Preliminary Checks

Test to check whether the available care workers data is sufficient to satisfy the bookings in a given time frame

##Prerequisites
#### Python libraries
Install python libraries in the requirements file in the preliminary test branch
```bash
#installing pip requirements
pip install -r requirements.txt

```
## Final File
data_suff_test_v5.py

### Flow of code

######For a period of consideration (period from given start date to end date):

Get the care workers and bookings valid for any duration in the period

#######For each day in the period:

Get care workers skills information and bookings on the day

########For each booking on the day:

#########For each slot in the booking:

Get simultaneous bookings

##########For each skill required in the booking:

Find whether there is insufficiency in skill, if so update solution list


