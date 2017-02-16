#!/usr/bin/env python
# -*- coding: utf_8 -*-
import os
import io
import time
import datetime
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
from flask import render_template

import core.settings as settings
import core.utils as utils

from core.scanner import general_code_analysis
from database import db_session
from models import Results


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config['DEBUG'] = settings.DEBUG
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.template_filter('slugify')
def _slugify(string):
    if not string:
        return ""
    return utils.slugify(string)


@app.context_processor
def _year():
    return dict(year=str(utils.year()))


@app.template_filter('js_escape')
def _js_escape(string):
    if not string:
        return ""
    return utils.js_escape(string)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def index():
    context = {'title': 'NodeJSScan V2'}
    return render_template("index.html", **context)


@app.route('/upload/', methods=['POST'])
def upload():
    """Upload Zipped Source"""
    if 'file' in request.files:
        filen = request.files['file']
        _, extension = os.path.splitext(filen.filename.lower())
        # Check for Valid ZIP
        if (filen and
                    filen.filename and
                    extension in settings.UPLD_ALLOWED_EXTENSIONS and
                    filen.mimetype in settings.UPLD_MIME
                ):
            filename = secure_filename(filen.filename)
            # Make upload dir
            if not os.path.exists(settings.UPLOAD_FOLDER):
                os.makedirs(settings.UPLOAD_FOLDER)
            # Save file
            zip_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filen.save(zip_file)
            # Get zip hash
            get_zip_hash = utils.gen_sha256_file(zip_file)
            # check if already scanned
            res = Results.query.filter(Results.scan_hash == get_zip_hash)
            if not res.count():
                # App analysis dir
                app_dir = os.path.join(
                    app.config['UPLOAD_FOLDER'], get_zip_hash + "/")
                # Make app analysis dir
                if not os.path.exists(app_dir):
                    os.makedirs(app_dir)
                # Unzip
                utils.unzip(zip_file, app_dir)
                # Do scan
                scan_results = general_code_analysis([app_dir])
                print "[INFO] Static Analysis Completed!"
                _, sha2_hashes, hash_of_sha2 = utils.gen_hashes([app_dir])
                tms = datetime.datetime.fromtimestamp(
                    time.time()).strftime('%Y-%m-%d %H:%M:%S')
                # Save Result
                print "[INFO] Saving Scan Results!"
                res_db = Results(get_zip_hash,
                                 [app_dir],
                                 sha2_hashes,
                                 hash_of_sha2,
                                 scan_results['sec_issues'],
                                 scan_results['good_finding'],
                                 scan_results['missing_sec_header'],
                                 scan_results['files'],
                                 scan_results['total_count'],
                                 scan_results['vuln_count'],
                                 [],
                                 [],
                                 tms,
                                 )
                db_session.add(res_db)
                db_session.commit()
            return jsonify({"status": "success", "url": "result/" + get_zip_hash})
    return jsonify({"status": "error", "desc": "Upload Failed!"})


@app.route('/dashboard/', methods=['GET'])
def dashboard():
    """Display dashboard"""
    context = {}
    res_shas = []
    ress = Results.query.all()
    for res in ress:
        locations = res.locations
        res_shas.append({"scan_hash": res.scan_hash,
                         "locations": locations,
                         "timestamp": str(res.timestamp),
                         }
                        )
    context = {
        'title': "Scan Dashboard",
        'scan_details': res_shas,

    }
    return render_template("dashboard.html", **context)


@app.route('/result/<regex("[0-9a-f]{64}"):sha2>/', methods=['GET'])
def result(sha2):
    res = Results.query.filter(Results.scan_hash == sha2).first()
    if res:
        locations = utils.python_list(res.locations)
        context = {'title': 'Scan Result',
                   'locations': locations,
                   'scan_hash': res.scan_hash,
                   'sha2_hashes': utils.python_list(res.sha2_hashes),
                   'security_issues': utils.python_dict(res.sec_issues),
                   'missing_headers': utils.python_dict(res.missing_sec_header),
                   'good_findings': utils.python_dict(res.good_finding),
                   'all_files': utils.python_list(res.files),
                   'total_count': utils.python_dict(res.total_count),
                   'vuln_n_count': utils.python_dict(res.vuln_count),
                   'resolved': utils.python_list(res.resolved),
                   'invalid': utils.python_list(res.invalid),
                   }
        return render_template("result.html", **context)
    else:
        return jsonify({"error": "scan_not_found"})


@app.route('/resolve', methods=['POST'])
def resolve():
    """Mark if it's not an issue"""
    scan_hash = request.form["scan_hash"]
    finding_hash = request.form["finding_hash"]
    if utils.sha2_match_regex(scan_hash) and utils.sha2_match_regex(finding_hash):
        res = Results.query.filter(Results.scan_hash == scan_hash)
        if res.count():
            reslvd = utils.python_list(res[0].resolved)
            if finding_hash not in reslvd:
                reslvd.append(finding_hash)
                res.update({"resolved": reslvd})
                db_session.commit()
                return jsonify({"status": "ok"})
    return jsonify({"status": "failed"})


@app.route('/revert', methods=['POST'])
def revert():
    """Revert not an issue to issue"""
    scan_hash = request.form["scan_hash"]
    finding_hash = request.form["finding_hash"]
    if utils.sha2_match_regex(scan_hash) and utils.sha2_match_regex(finding_hash):
        res = Results.query.filter(Results.scan_hash == scan_hash)
        if res.count():
            reslvd = utils.python_list(res[0].resolved)
            if finding_hash in reslvd:
                reslvd.remove(finding_hash)
                res.update({"resolved": reslvd})
                db_session.commit()
                return jsonify({"status": "ok"})
    return jsonify({"status": "failed"})


@app.route('/invalid', methods=['POST'])
def invalid():
    """Mark the issue as invalid"""
    scan_hash = request.form["scan_hash"]
    invalid_hash = request.form["invalid_hash"]
    if utils.sha2_match_regex(scan_hash) and utils.sha2_match_regex(invalid_hash):
        res = Results.query.filter(Results.scan_hash == scan_hash)
        if res.count():
            invld = utils.python_list(res[0].invalid)
            if invalid_hash not in invld:
                invld.append(invalid_hash)
                res.update({"invalid": invld})
                db_session.commit()
                return jsonify({"status": "ok"})
    return jsonify({"status": "failed"})


@app.route('/view_file', methods=['POST'])
def view_file():
    """View File"""
    context = {"contents": "not_found"}
    path = request.form["path"]
    scan_hash = request.form["scan_hash"]
    if utils.sha2_match_regex(scan_hash):
        res = Results.query.filter(Results.scan_hash == scan_hash).first()
        if res:
            _, extension = os.path.splitext(path.lower())
            if ((extension in settings.SCAN_FILES_EXTENSION) and
                    (not utils.is_attack_pattern(path))
                    ):
                path = os.path.join(settings.UPLOAD_FOLDER, path)
                if os.path.isfile(path):
                    contents = utils.unicode_safe_file_read(path)
                    context = {"contents": contents}
    return jsonify(**context)


@app.route('/search', methods=['POST'])
def search():
    """Search in source files."""
    matches = []
    context = {}
    query = request.form['q']
    scan_hash = request.form["scan_hash"]
    context = {'contents': 'not_found',
               'matches': matches,
               'term': query,
               'found': '0',
               'scan_hash': ''}
    if utils.sha2_match_regex(scan_hash):
        res = Results.query.filter(Results.scan_hash == scan_hash).first()
        if res:
            locations = utils.python_list(res.locations)
            for loc in locations:
                for dir_name, _, files in os.walk(loc):
                    for jfile in files:
                        _, extension = os.path.splitext(jfile.lower())
                        if extension in settings.SCAN_FILES_EXTENSION:
                            file_path = os.path.join(loc, dir_name, jfile)
                            fileparam = file_path.replace(
                                settings.UPLOAD_FOLDER, '')
                            with io.open(
                                file_path,
                                mode='r',
                                encoding="utf8",
                                errors="ignore"
                            ) as file_pointer:
                                dat = file_pointer.read()
                            if query in dat:
                                matches.append(
                                    {"name": jfile, "path": fileparam})
            context = {
                'title': 'Search Results',
                'matches': matches,
                'term': query,
                'found': len(matches),
                'scan_hash': scan_hash,
            }
    return render_template("search.html", **context)

if __name__ == '__main__':
    app.run(threaded=True,
            host=settings.HOST,
            port=settings.PORT)
