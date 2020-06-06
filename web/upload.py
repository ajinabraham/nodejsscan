#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Handle file upload."""
import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

from werkzeug.utils import secure_filename

from flask import jsonify

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
    print('\n[INFO] Unzipping file', file=sys.stderr)
    try:
        if not os.path.exists(ext_path):
            os.makedirs(ext_path)
        with zipfile.ZipFile(app_path, 'r') as ptr:
            ptr.extractall(ext_path)
    except Exception:
        print('[ERROR] Unzipping with Python API')
        print('\n[INFO] Using the default OS unzip utility.', file=sys.stderr)
        try:
            subprocess.call([
                shutil.which('unzip'),
                '-o',
                '-q',
                app_path,
                '-d',
                ext_path])
        except Exception:
            print('[ERROR] Unzipping from zip file')


def handle_upload(app, files):
    """Handle File Upload."""
    failed = {
        'status': 'failed',
        'message': 'Upload Failed!'}
    if 'file' not in files:
        return jsonify(failed)
    filen = files['file']
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
    return jsonify({
        'status': 'success',
        'url': 'scan/' + sha2})
