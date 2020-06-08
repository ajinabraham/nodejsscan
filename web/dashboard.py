#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Function related to dashboard."""
import copy
import shutil
from pathlib import Path

from flask import (
    jsonify,
    render_template,
)

from nodejsscan import (
    filters,
    nodejsscan,
    settings,
    utils,
)

from web.db_operations import (
    delete_scan,
    get_results,
    get_scans,
    update_issue,
)


# Templates
def home():
    """Home."""
    context = {
        'mimes': settings.UPLD_MIME,
        'version': settings.VERSION,
        'year': utils.year(),
    }
    return render_template('index.html', **context)


def scans():
    """Recent Scans view in nodejsscan."""
    context = get_scans()
    context['version'] = settings.VERSION
    context['year'] = utils.year()
    return render_template('scans.html', **context)


def scan_result(sha2):
    """Get Scan result."""
    res = get_results(sha2)
    if not res:
        return jsonify({
            'status': 'failed',
            'message': 'Scan hash not found'})
    triage = filters.get_triaged(res)
    filters.filter_files(res, 'nodejs')
    filters.filter_files(res, 'templates')
    new_dict = copy.deepcopy(res)
    filters.filter_rules(res, new_dict, 'nodejs')
    filters.filter_rules(res, new_dict, 'templates')
    new_dict['version'] = settings.VERSION
    new_dict['year'] = utils.year()
    sev, isus = filters.get_metrics(new_dict)
    new_dict['severity'] = sev
    new_dict['security_issues'] = isus
    new_dict['triaged'] = triage
    return render_template('scan_result.html', **new_dict)


def search_file(request):
    """Search in files."""
    context = {}
    query = request.form['q']
    scan_hash = request.form['scan_hash']
    if not utils.issha2(scan_hash):
        return jsonify({
            'status': 'failed',
            'message': 'Scan hash not found'})
    res = get_results(scan_hash)
    if not res:
        return jsonify({
            'status': 'failed',
            'message': 'Scan hash not found'})
    matches = nodejsscan.all_files(res['location'], True, query)
    context = {
        'matches': matches,
        'term': query,
        'scan_hash': scan_hash,
        'version': settings.VERSION,
        'year': utils.year(),
    }
    return render_template('search.html', **context)


# APIs
def scan_delete(request):
    """Delete Scan results from DB."""
    scan_hash = request.form['scan_hash']
    if not utils.issha2(scan_hash):
        return jsonify(**{
            'status': 'failed',
            'message': 'Invalid scan hash'})
    res = delete_scan(scan_hash)
    if not res:
        return jsonify(**{
            'status': 'failed',
            'message': 'Scan not found'})
    shutil.rmtree(res.location)
    if res.scan_file.endswith('.zip'):
        ziploc = Path(settings.UPLOAD_FOLDER) / res.scan_file
        ziploc.unlink()
    return jsonify(**{'status': 'ok'})


def issue_revert(request):
    """Revert FP/NA."""
    scan_hash = request.form['scan_hash']
    finding_hash = request.form['finding_hash']
    if not (utils.issha2(scan_hash) and utils.issha2(finding_hash)):
        return jsonify(**{
            'status': 'failed',
            'message': 'Invalid hash'})
    res = get_results(scan_hash)
    if not res:
        return jsonify({
            'status': 'failed',
            'message': 'Scan hash not found'})
    fp_key = 'false_positive'
    na_key = 'not_applicable'
    fp = res[fp_key]
    na = res[na_key]
    if finding_hash in fp:
        fp.remove(finding_hash)
        update_issue(scan_hash, fp_key, fp)
    elif finding_hash in na:
        na.remove(finding_hash)
        update_issue(scan_hash, na_key, na)
    else:
        return jsonify({
            'status': 'failed',
            'message': 'Finding not found'})
    return jsonify({'status': 'ok'})


def issue_hide(request, issue_type):
    """Issue is FP/NA."""
    scan_hash = request.form['scan_hash']
    finding_hash = request.form['id']
    if not (utils.issha2(scan_hash) and utils.issha2(finding_hash)):
        return jsonify({
            'status': 'failed',
            'message': 'Invalid hash'})
    res = get_results(scan_hash)
    if not res:
        return jsonify({
            'status': 'failed',
            'message': 'Scan hash not found'})
    if issue_type == 'fp':
        key = 'false_positive'
    else:
        key = 'not_applicable'
    item = res[key]
    if finding_hash not in item:
        item.append(finding_hash)
        update_issue(scan_hash, key, item)
    return jsonify({'status': 'ok'})


def view_file(request):
    """View a File."""
    context = {'contents': 'not_found'}
    path = request.form['path']
    scan_hash = request.form['scan_hash']
    if not utils.issha2(scan_hash):
        return jsonify({
            'status': 'failed',
            'message': 'Invalid hash'})
    res = get_results(scan_hash)
    if not res:
        return jsonify({
            'status': 'failed',
            'message': 'Scan hash not found'})
    safe_dir = settings.UPLOAD_FOLDER
    req_path = Path(safe_dir) / path
    if not utils.is_safe_path(safe_dir, req_path.as_posix()):
        context = {
            'status': 'failed',
            'contents': 'Path Traversal Detected!'}
    else:
        if req_path.is_file():
            contents = utils.read_file(req_path.as_posix())
            context = {'contents': contents}
    return jsonify(**context)
