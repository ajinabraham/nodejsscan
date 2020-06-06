#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Integration: njsscan."""
import os
from pathlib import Path

from nodejsscan import (
    settings,
    utils,
)

from njsscan.njsscan import NJSScan
from njsscan.settings import (
    IGNORE_PATHS,
    NODEJS_FILE_EXTENSIONS,
    TEMPLATE_FILE_EXTENSIONS,
)


def all_files(path):
    """Gather all files and hashes."""
    filelist = []
    supported_ext = NODEJS_FILE_EXTENSIONS.union(TEMPLATE_FILE_EXTENSIONS)
    # TODO replace with pathlib
    for root, _, files in os.walk(path):
        for filename in files:
            full_file_path = os.path.join(root, filename)
            if any(ignore in full_file_path
                    for ignore in IGNORE_PATHS):
                continue
            if Path(full_file_path).suffix in supported_ext:
                mpath = full_file_path.replace(
                    settings.UPLOAD_FOLDER, '', 1)
                if mpath.startswith('/'):
                    mpath = mpath.replace('/', '', 1)
                filelist.append(mpath)
    return filelist


def call_njsscan(node_source):
    """Call njsscan."""
    scanner = NJSScan([node_source], json=True, check_controls=True)
    return scanner.scan()


def add_ids(res):
    """Add hash to findings."""
    if not res:
        return
    for rule, finds in res.items():
        if not finds.get('files'):
            res[rule]['id'] = utils.sha256_finding(finds)
            continue
        for file in finds['files']:
            file['id'] = utils.sha256_finding(file)


def scan(node_source):
    """Perform scan."""
    result = call_njsscan(node_source)
    add_ids(result.get('nodejs'))
    add_ids(result.get('templates'))
    result['files'] = all_files(node_source)
    return result
