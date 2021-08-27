#!/bin/bash
db_name=$1
db_user='postgres'
host='hcms-db.caoy9b44uned.ap-southeast-1.rds.amazonaws.com'
port='5432'
db_dump_path=$2
db_pass=$3

echo "Initiating Refresh DB"
echo "Dropping connections.."
## Drop all connections
PGPASSWORD=${db_pass} psql -h ${host} -p ${port} -U ${db_user} -c "REVOKE CONNECT ON DATABASE ${db_name} FROM public;"
PGPASSWORD=${db_pass} psql -h ${host} -p ${port} -U ${db_user} -c "SELECT pg_terminate_backend (pid) FROM pg_stat_activity WHERE datname='${db_name}'"

echo "Dropping database.."
PGPASSWORD=${db_pass} psql -h ${host} -p ${port} -U ${db_user} -c "Drop database ${db_name}"

echo "Creating database.."
PGPASSWORD=${db_pass} psql -h ${host} -p ${port} -U ${db_user} -c "Create database ${db_name}"

echo "Restoring database.."
PGPASSWORD=${db_pass} psql -h ${host} -p ${port} -U ${db_user} -d ${db_name} -f ${db_dump_path}

echo "Refresh database done"
exit 0
