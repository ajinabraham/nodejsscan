#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Slack integration."""
import os
from threading import Thread

import requests


from nodejsscan import (
    filters,
    settings,
    utils,
)


def slack_post(url, slack_json):
    """Send slack POST."""
    requests.post(url, json=slack_json)


def slack_alert(filename, sha2, base_url, message):
    """Send slack alert."""
    url = os.environ.get(
        'SLACK_WEBHOOK_URL', settings.SLACK_WEBHOOK_URL)
    if not url:
        return
    severity, total_issues = filters.get_metrics(message)
    total_files = len(message['files'])
    scan_file = filename
    error = severity['error']
    warning = severity['warning']
    info = severity['info']
    slack_json = {
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'*nodejsscan v{settings.VERSION}*',
                },
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'text': ('Scan Completed '
                                 f'on: *{utils.get_timestamp()}*'),
                        'type': 'mrkdwn',
                    },
                ],
            },
            {
                'type': 'divider',
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': (f'Found *{total_issues}* issues'
                             f' in *{total_files}* files :zap:'),
                },
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'nodejsscan finished analyzing *{ scan_file }*',
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'See Scan Results',
                    },
                    'url': f'{base_url}scan/{sha2}',
                    'style': 'primary',
                },
            },
            {
                'type': 'divider',
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '*Severity Distribution*',
                },
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f':octagonal_sign: ERROR: *{error}*',
                },
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f':warning: WARNING: *{warning}*',
                },
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f':information_source: INFO: *{info}*',
                },
            },
            {
                'type': 'divider',
            },
        ],
    }
    process = Thread(target=slack_post, args=(url, slack_json))
    process.start()
    process.join()
