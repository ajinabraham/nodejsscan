#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Handle file upload."""
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

from werkzeug.utils import secure_filename

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


def unzip(app_path, ext_path):
    """Unzip files to a given path."""
    print('[INFO] Unzipping file', file=sys.stderr)
    try:
        ext_path = Path(ext_path)
        if not ext_path.exists():
            ext_path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(app_path.as_posix(), 'r') as ptr:
            ptr.extractall(ext_path.as_posix())
    except Exception:
        print('[ERROR] Unzipping with Python API')
        print('[INFO] Using the default OS unzip utility.', file=sys.stderr)
        try:
            subprocess.call([
                shutil.which('unzip'),
                '-o',
                '-q',
                app_path,
                '-d',
                ext_path.as_posix()])
        except Exception:
            print('[ERROR] Unzipping from zip file')


def handle_upload(app, request):
    """Handle File Upload."""
    failed = {
        'status': 'failed',
        'message': 'Upload Failed!'}
    if 'file' not in request.files:
        return jsonify(failed)
    filen = request.files['file']
    ext = Path(filen.filename.lower()).suffix
    # Check for Valid ZIP
    if not (ext in '.zip' and filen.mimetype in settings.UPLD_MIME):
        return jsonify(failed)
    filename = secure_filename(filen.filename)
    # Save file
    zip_file = Path(app.config['UPLOAD_FOLDER']) / filename
    filen.save(zip_file)
    # Get zip hash
    sha2 = utils.gen_sha256_file(zip_file)
    # Check if already scanned
    if is_scan_exists(sha2):
        return jsonify({
            'status': 'success',
            'url': 'scan/' + sha2})
    # App analysis dir
    app_dir = Path(app.config['UPLOAD_FOLDER']) / sha2
    # Make app analysis dir
    if not app_dir.exists():
        app_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
    app_dir = app_dir.as_posix()
    # Unzip
    unzip(zip_file, app_dir)
    # Do scan
    results = nodejsscan.scan(app_dir)
    # Save Result
    print('[INFO] Saving Scan Results!')
    save_results(filename, sha2, app_dir, results)
    slack_alert(filename, sha2, request.url_root, results)
    email_alert(filename, sha2, request.url_root, results)
    return jsonify({
        'status': 'success',
        'url': 'scan/' + sha2})
