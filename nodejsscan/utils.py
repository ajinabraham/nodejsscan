#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Util and helper functions."""
from datetime import datetime
import hashlib
import json
import time
import os
import re
import ast
import unicodedata

from werkzeug.routing import BaseConverter

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def read_file(file_path):
    """Read a file in an unicode safe way."""
    with open(file_path, 'rb') as file_ptr:
        return file_ptr.read().decode('utf-8', 'replace')


def issha2(data):
    """Check for a SHA2 string match."""
    return re.match('^[0-9a-f]{64}$', data)


def python_list(value):
    """Convert a list like string to a Python list."""
    if not value:
        value = []
    if isinstance(value, list):
        return value
    return ast.literal_eval(value)


def python_dict(value):
    """Convert a dict like string to Python dict."""
    if not value:
        value = {}
    if isinstance(value, dict):
        return value
    return ast.literal_eval(value)


def gen_sha256_hash(msg):
    """Generate the SHA256 hash of a message."""
    hash_object = hashlib.sha256(msg.encode('utf-8'))
    return hash_object.hexdigest()


def gen_sha256_file(path):
    """Generate the SHA 256 hash of a file."""
    blocksize = 64 * 1024
    sha = hashlib.sha256()
    with open(path, 'rb') as fptr:
        while True:
            data = fptr.read(blocksize)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def sha256_finding(find_dict):
    """Generate hash of the finding."""
    return gen_sha256_hash(json.dumps(find_dict, sort_keys=True))


def year():
    """Get the current year."""
    now = datetime.now()
    return now.year


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punctuation_re.split(text.lower()):
        word = unicodedata.normalize(
            'NFKD', word).encode(
                'ascii', 'ignore').decode('utf-8')
        if word:
            result.append(word)
    return delim.join(result)


def deslugify(text):
    """Reverse Slugify."""
    normalized = ''
    items = text.split('_')
    for item in items:
        normalized += item.capitalize() + ' '
    return normalized


def js_escape(value):
    """Javascript XSS escapes."""
    return (value.replace('<', '\\u003c').
            replace('>', '\\u003e').
            replace('"', '\\u0022').
            replace('\'', '\\u0027').
            replace('`', '\\u0060').
            replace('(', '\\u0028').
            replace(')', '\\u0029').
            replace('{', '\\u007b').
            replace('}', '\\u007d').
            replace('-', '\\u002d').
            replace('+', '\\u007d').
            replace('$', '\\u0024').
            replace('/', '\\u002f'))


def is_safe_path(safe_root, check_path):
    """Detect Path Traversal."""
    safe_root = os.path.realpath(os.path.normpath(safe_root))
    check_path = os.path.realpath(os.path.normpath(check_path))
    return os.path.commonprefix([check_path, safe_root]) == safe_root


def get_timestamp():
    """Get timestamp."""
    return datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
