#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""The nodejsscan webapp."""
import re

from werkzeug.routing import BaseConverter

from flask import Flask, request

import nodejsscan.settings as settings
import nodejsscan.utils as utils

from web.upload import handle_upload
from web.dashboard import (
    home,
    issue_hide,
    issue_revert,
    scan_delete,
    scan_result,
    scans,
    search_file,
    view_file,
)

from migrate import db_session


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
        return ''
    return utils.slugify(string)


@app.template_filter('deslugify')
def _deslugify(string):
    if not string:
        return ''
    return utils.deslugify(string)


@app.template_filter('relative')
def relative(string):
    if not string:
        return ''
    result = re.compile(r'[A-Fa-f0-9]{64}[/\\]').search(string)
    if not result:
        return string
    return string.split(result.group(0), 1)[1]


@app.context_processor
def _year():
    return dict(year=str(utils.year()))


@app.template_filter('js_escape')
def _js_escape(string):
    if not string:
        return ''
    return utils.js_escape(string)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def index():
    """Handle Index."""
    return home()


@app.route('/upload/', methods=['POST'])
def upload():
    """Upload and unzip source."""
    return handle_upload(app, request.files)


@app.route('/scans/', methods=['GET'])
def allscans():
    """Display list of scans."""
    return scans()


@app.route('/scan/<regex(r\'[0-9a-f]{64}\'):sha2>/', methods=['GET'])
def scan(sha2):
    """Show a scan result."""
    return scan_result(sha2)


@app.route('/delete_scan', methods=['POST'])
def delete_scan():
    """Delete Scan result."""
    return scan_delete(request)


@app.route('/revert', methods=['POST'])
def revert():
    """Revert not an issue to issue."""
    return issue_revert(request)


@app.route('/false_positive', methods=['POST'])
def false_positive():
    """Mark the issue as fasle_positive."""
    return issue_hide(request, 'fp')


@app.route('/not_applicable', methods=['POST'])
def not_applicable():
    """Mark the issue as fasle_positive."""
    return issue_hide(request, 'na')


@app.route('/view_file', methods=['POST'])
def view():
    return view_file(request)


@app.route('/search', methods=['POST'])
def search():
    """Search in source files."""
    return search_file(request)


if __name__ == '__main__':
    app.run(threaded=True,
            debug=settings.DEBUG,
            host=settings.HOST,
            port=settings.PORT)
