#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Git scanning."""
from pathlib import Path
from urllib.parse import urlparse

import git

from flask import jsonify

from web.slack import slack_alert
from web.email import email_alert

from nodejsscan import (
    nodejsscan,
    settings,
    utils,
)

from web.db_operations import (
    is_scan_exists,
    save_results,
)


def lsremote(url):
    """Git ls-remote."""
    remote_refs = {}
    g = git.cmd.Git()
    for ref in g.ls_remote(url).split('\n'):
        hash_ref_list = ref.split('\t')
        remote_refs[hash_ref_list[1]] = hash_ref_list[0]
    return remote_refs


def clone(request):
    """Git clone."""
    url = request.form['url']
    if not url.endswith('.git'):
        return jsonify({
            'status': 'failed',
            'message': 'Please provide a valid git URL!'})
    try:
        refs = lsremote(url)
    except Exception as exp:
        return jsonify({
            'status': 'failed',
            'message': str(exp)})
    sha2 = utils.gen_sha256_hash(refs['HEAD'])
    app_dir = Path(settings.UPLOAD_FOLDER) / sha2
    if is_scan_exists(sha2):
        return jsonify({
            'status': 'success',
            'url': 'scan/' + sha2})
    if not app_dir.exists():
        print('[INFO] Cloning Repository')
        git.Repo.clone_from(url, app_dir.as_posix())
    results = nodejsscan.scan(app_dir.as_posix())
    # Save Result
    print('[INFO] Saving Scan Results!')
    filename = Path(urlparse(url).path).name
    save_results(filename, sha2, app_dir.as_posix(), results)
    slack_alert(filename, sha2, request.url_root, results)
    email_alert(filename, sha2, request.url_root, results)
    return jsonify({
        'status': 'success',
        'url': 'scan/' + sha2})
