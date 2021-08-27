# !/bin/bash
echo Get Token
curl --header "Content-Type: application/json" --request POST  --data '{"user":{"user_name":"root", "password":"toor"}}'  localhost:8000/api/auth/login > data/token

echo import groups, password: root
echo -----------------------------
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/auth_group.csv 

echo import cw
echo ----------
python data/cw_load.py

echo import su
echo -----------------------------
python data/su_load.py

echo import master codes, password: root
echo -----------------------------
mysql -u root -p populated_db_1 < data/hcms_utils_master_code.sql

echo import languages, availability, preferences,performance, salary details, password: root
echo --------------------------------------------------------------------------------------------
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/hcms_um_language.csv
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/hcms_su_preference.csv
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/hcms_cw_preference.csv
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/hcms_performance.csv
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/hcms_alerts_rules.csv
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/hcms_alerts_trigger.csv
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u "root" -p  populated_db_1 data/hcms_cw_salary_detail.csv

echo import avail
echo -----------------------------
python data/cw_avail_load.py 

echo import booking
echo -----------------------------
python data/booking_load.py 

echo other users
echo -----------------------------
python manage.py shell <shell_script.py


python manage.py crontab add
python manage.py crontab add