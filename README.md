# HCMS : Backend
Run the following commands sequentially.


## Code base


```bash
git clone https://github.com/cysren/hcms-backend.git
```

## Prerequisites 

#### Applications
- Apache 
- Postgres
- Daphne
- Redis

#### Python libraries
```bash
#installing pip requirements
pip install -r requirements.txt

```

## DB Setup

- Create the initial database and travel time database.

- Set the database names in the code base.

- Initialize following tables
  - Followup
  - Triggers
  - Rules
  - Master Codes
  - Config Codes

- Migrations
```bash
python manage.py migrate
```


## System Setup

### Start Apache
```bash
sudo systemctl start apache2
```

### Restart Apache
```bash
./restart.sh
```

### Setup daphne server
```bash
daphne -v2 -u /tmp/daphne.sock -b 0.0.0.0 -p <port> hcms.asgi:application
```

### Process tasks
```bash
python3 manage.py process_tasks
```

### Cron tab

```bash
python manage.py crontab add
```
