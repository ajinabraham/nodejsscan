#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Settings for nodejsscan."""
from pathlib import Path

# GENERAL
VERSION = '4'
UPLOAD_FOLDER = Path('~/.nodejsscan/').expanduser().as_posix()
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
UPLD_MIME = [
    'application/zip',
    'application/octet-stream',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
IGNORE_PATHS = ('.git', '.DS_Store')
CHECK_MISSING_CONTROLS = True

# Postgres DB Connection URL
SQLALCHEMY_DATABASE_URI = 'postgresql://127.0.0.1/nodejsscan'

# Get Slack alerts
SLACK_WEBHOOK_URL = ''

# Get Email alerts
NJS_FROM_EMAIL = ''
NJS_TO_EMAIL = ''
SMTP_SERVER = ''
SMTP_PORT = None
SMTP_STARTTLS = False
SMTP_USER = ''
SMTP_PASS = ''
