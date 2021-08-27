#!/bin/bash
rm nohup.out
ps aux | grep process_tasks
echo "Killing.."
sudo pkill -f "python manage.py process_tasks"
sudo pkill -f "daphne"
ps aux | grep process_tasks
echo "Restart.."
sudo systemctl restart apache2
nohup python manage.py process_tasks &
nohup daphne -v2 -u /tmp/daphne.sock -b 0.0.0.0 -p 9090 hcms.asgi:application > sock.out 2>sock.err &
echo "Process Tasks.."
ps aux | grep process_tasks
echo "Restart done"
