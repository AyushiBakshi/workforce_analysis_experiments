# !/bin/bash

echo Delete exsisting DB, password: root
echo ------------------------------------
mysqladmin -h localhost -u root -p drop populated_db_1

# rm -rf booking/migrations/
# rm -rf cw/migrations/
# rm -rf su/migrations/
# rm -rf users/migrations/
# rm -rf utils/migrations/
# rm -rf performance/migrations/
# rm -rf incident/migrations/
# rm -rf complaint/migrations/
# rm -rf alerts/migrations/
# rm -rf cron/migrations/

# rm -rf booking/__pycache__/
# rm -rf cw/__pycache__/
# rm -rf su/__pycache__/
# rm -rf users/__pycache__/
# rm -rf performance/__pycache__/
# rm -rf complaint/__pycache__/
# rm -rf incident/__pycache__/
# rm -rf alerts/__pycache__/
# rm -rf cron/__pycache__/

echo Create Raw DB, password: root
echo -----------------------------
mysql -u root -p -e "create database populated_db_1"; 


echo Migrations
echo -----------

python manage.py makemigrations complaint;
python manage.py makemigrations incident;
python manage.py makemigrations performance;
python manage.py makemigrations su;
python manage.py makemigrations cw;
python manage.py makemigrations booking;
python manage.py makemigrations users;
python manage.py makemigrations utils;
python manage.py makemigrations alerts;
python manage.py makemigrations cron;

python manage.py migrate;

echo Create super user ,user: root, email: root@root.com, password: toor
echo -------------------------------------------------------------------
python manage.py createsuperuser;

echo Runserver
echo ----------
python manage.py runserver;

