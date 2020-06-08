#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Integration: njsscan."""
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


def all_files(path, search=False, term=None):
    """Gather all files or search."""
    filelist = []
    ignote_paths = IGNORE_PATHS.union(settings.IGNORE_PATHS)
    supported_ext = NODEJS_FILE_EXTENSIONS.union(TEMPLATE_FILE_EXTENSIONS)
    for file_path in Path(path).rglob('*'):
        if not file_path.is_file():
            continue
        if file_path.suffix not in supported_ext:
            continue
        if any(ignore in file_path.as_posix()
                for ignore in ignote_paths):
            continue
        relative = file_path.as_posix().replace(
            settings.UPLOAD_FOLDER, '', 1)
        if relative.startswith('/'):
            relative = relative.replace('/', '', 1)
        if search:
            if term in utils.read_file(file_path.as_posix()):
                filelist.append(relative)
        else:
            filelist.append(relative)
    return filelist


def call_njsscan(node_source):
    """Call njsscan."""
    scanner = NJSScan(
        [node_source],
        json=True,
        check_controls=settings.CHECK_MISSING_CONTROLS)
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
    print('[INFO] Performing Static Analysis')
    result = call_njsscan(node_source)
    add_ids(result.get('nodejs'))
    add_ids(result.get('templates'))
    result['files'] = all_files(node_source)
    return result
