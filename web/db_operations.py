#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""All DB operations."""
import nodejsscan.utils as utils
from nodejsscan.models import (
    ScanResults,
    db,
)


def save_results(filename, sha256, location, results):
    """Save Scan Results."""
    res = ScanResults(
        filename,
        sha256,
        location,
        results['nodejs'],
        results['templates'],
        results['files'],
        [],
        [],
        utils.get_timestamp())
    db.session.add(res)
    db.session.commit()


def get_scans():
    """Get all scans."""
    context = {}
    res_shas = []
    ress = ScanResults.query.all()
    for res in ress:
        res_shas.append({
            'scan_hash': res.scan_hash,
            'scan_file': res.scan_file,
            'timestamp': str(res.timestamp)})
    res_shas.reverse()
    context = {
        'scan_details': res_shas,
    }
    return context


def get_results(sha256):
    """Read Scan Results."""
    res = ScanResults.query.filter(ScanResults.scan_hash == sha256).first()
    if res:
        context = {
            'title': 'Scan Result',
            'scan_file': res.scan_file,
            'scan_hash': res.scan_hash,
            'location': res.location,
            'nodejs': utils.python_dict(res.nodejs),
            'templates': utils.python_dict(res.templates),
            'files': utils.python_list(res.files),
            'false_positive': utils.python_list(res.false_positive),
            'not_applicable': utils.python_list(res.not_applicable),
        }
        return context
    return None


def update_issue(sha256, key, item):
    """Get Result obj by hash."""
    res = ScanResults.query.filter(ScanResults.scan_hash == sha256)
    res.update({key: item})
    db.session.commit()


def is_scan_exists(sha256):
    """Check if already scanned."""
    return ScanResults.query.filter(ScanResults.scan_hash == sha256).first()


def delete_scan(sha256):
    """Delete scan by hash."""
    res = ScanResults.query.filter(ScanResults.scan_hash == sha256).first()
    if res:
        db.session.delete(res)
        db.session.commit()
    return res
