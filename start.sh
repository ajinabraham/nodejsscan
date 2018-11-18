#!/usr/bin/env bash
setsid docker-entrypoint.sh postgres >/dev/fd/1 2>&1 < /dev/fd/1 &

sleep 10
python3 migrate.py
gunicorn -b 0.0.0.0:9090 app:app --workers 3 --timeout 10000
