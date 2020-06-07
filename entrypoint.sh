#!/usr/bin/env bash
setsid docker-entrypoint.sh postgres >/dev/fd/1 2>&1 < /dev/fd/1 &

sleep 10
/usr/bin/python3.7 manage.py recreate_db
/usr/local/bin/gunicorn -b 0.0.0.0:9090 nodejsscan.app:app --workers=1 --threads=10 --timeout 1800