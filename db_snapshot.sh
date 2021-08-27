#!/bin/bash
db_name=$1
db_user='postgres'
host='hcms-db.caoy9b44uned.ap-southeast-1.rds.amazonaws.com'
port='5432'
db_snapshot_path=$2
db_pass=$3

# Initiating capturing of database snapshot
PGPASSWORD=${db_pass} pg_dump -h ${host} -p ${port} -U ${db_user} -f ${db_snapshot_path} ${db_name}
