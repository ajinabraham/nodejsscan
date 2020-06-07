#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Filter Results."""
import copy


def triage_files(fp, na, res, rule, finds):
    """Get triaged files."""
    na_list = []
    fp_list = []
    na_finds = copy.deepcopy(finds)
    fp_finds = copy.deepcopy(finds)
    for file in finds['files']:
        if file['id'] in res['false_positive']:
            fp_list.append(file)
        if file['id'] in res['not_applicable']:
            na_list.append(file)
    if na_list:
        na_finds['files'] = na_list
        na[rule] = na_finds
    if fp_list:
        fp_finds['files'] = fp_list
        fp[rule] = fp_finds


def get_triaged(res):
    """Get findings filterd by na/fp."""
    fp = {}
    na = {}
    combined = {}
    if res.get('templates'):
        combined.update(res['templates'])
    if res.get('nodejs'):
        combined.update(res['nodejs'])
    for rule, finds in combined.items():
        # No files means single rule with id
        file_less = finds.get('id')
        if file_less:
            if file_less in res['false_positive']:
                fp[rule] = finds
            elif file_less in res['not_applicable']:
                na[rule] = finds
            continue
        triage_files(fp, na, res, rule, finds)
    return {
        'fp': fp,
        'na': na,
    }


def inc_severity(severity_dict, severity):
    """Increment Siverity."""
    if severity.upper() == 'ERROR':
        severity_dict['error'] += 1
    elif severity.upper() == 'WARNING':
        severity_dict['warning'] += 1
    elif severity.upper() == 'INFO':
        severity_dict['info'] += 1


def get_metrics(res):
    """Get Severity and Issue counts."""
    issue_count = 0
    severity_dict = {
        'error': 0,
        'warning': 0,
        'info': 0,
    }
    combined = {}
    if res.get('templates'):
        combined.update(res['templates'])
    if res.get('nodejs'):
        combined.update(res['nodejs'])
    for _, finds in combined.items():
        if 'files' not in finds:
            issue_count += 1
        else:
            issue_count += len(finds['files'])
        inc_severity(severity_dict, finds['metadata']['severity'])
    return severity_dict, issue_count


def filter_files(res, key):
    """Remove FP/NA Files."""
    excludes = set(res['false_positive'] + res['not_applicable'])
    if res.get(key):
        for _, findings in res[key].items():
            if not findings.get('files'):
                continue
            tmp_files = copy.deepcopy(findings['files'])
            for file in findings['files']:
                if file['id'] in excludes:
                    tmp_files.remove(file)
            findings['files'] = tmp_files


def filter_rules(res, new_dict, key):
    """Remove FP/NA Rules."""
    excludes = set(res['false_positive'] + res['not_applicable'])
    if res.get(key):
        for rule, findings in res[key].items():
            if 'files' not in findings:
                if findings['id'] in excludes:
                    del new_dict[key][rule]
            elif len(findings['files']) == 0:
                del new_dict[key][rule]
