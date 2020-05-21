#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Util and helper functions."""
import zipfile
import string
import random
import sys
import linecache
import datetime
import hashlib
import ntpath
import hmac
import time
import json
import os
import os.path as osp
import re
import ast
import unicodedata
import subprocess
import core.settings as settings

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


class Color(object):
    """Coloring the terminal/Bash output."""
    GREEN = '\033[92m'
    ORANGE = '\033[33m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_exception(msg):
    """Print and log an exception."""
    _, exc_obj, tb_f = sys.exc_info()
    f_obj = tb_f.tb_frame
    lineno = tb_f.tb_lineno
    filename = f_obj.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f_obj.f_globals)
    timestamp = time.time()
    stringtime = datetime.datetime.fromtimestamp(
        timestamp).strftime('%Y-%m-%d %H:%M:%S')
    dat = '\n[' + stringtime + ']\n' + msg + \
        '\nFILE: {0}\nLINE: {1} - {2}\nDESC: {3}'.format(
            filename, lineno, line.strip(), exc_obj)
    print(Color.BOLD + Color.RED + dat + Color.END)
    with open(settings.LOG_FILE, 'a') as file_ptr:
        file_ptr.write(dat)


def unzip(app_path, ext_path):
    """Unzip files to a given path and return the list of files extracted."""
    print("\n[INFO] Unzipping from zip file", file=sys.stderr)
    try:
        if not os.path.exists(ext_path):
            os.makedirs(ext_path)
        files = []
        with zipfile.ZipFile(app_path, "r") as ptr:
            ptr.extractall(ext_path)
            files = ptr.namelist()
        return files
    except:
        print_exception("[ERROR] Unzipping from zip file with Python")
        print("\n[INFO] Using the default OS unzip utility.", file=sys.stderr)
        try:
            subprocess.call(['unzip', '-o', '-q', app_path, '-d', ext_path])
            dat = subprocess.check_output(['unzip', '-qq', '-l', app_path])
            dat = dat.split('\n')
            dat = ['Length   Date   Time   Name'] + dat
            return dat
        except:
            print_exception("[ERROR] Unzipping from zip file")


def read_file(file_path):
    """Read a file in an unicode safe way."""
    with open(file_path, "rb") as file_ptr:
        return file_ptr.read().decode('utf-8', 'replace')


def write_file(file_path, data):
    """Write a file in an Unicode safe way."""
    with open(file_path, "w") as file_ptr:
        file_ptr.write(data)


def sha2_match_regex(data):
    """Check for a SHA2 string match."""
    return re.match('^[0-9a-f]{64}$', data)


def is_number(strn):
    """Check if given string is a number."""
    try:
        float(strn)
        return True
    except ValueError:
        pass
    try:
        unicodedata.numeric(strn)
        return True
    except (TypeError, ValueError):
        pass
    return False


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


def gen_random_hmac_sha256(msg):
    """Generate the HMAC SHA256 of a message with random key."""
    key = hashlib.sha256(random.SystemRandom().random()).hexdigest()[:5]
    hashed = hmac.new(key, msg, hashlib.sha256)
    return hashed.hexdigest()


def gen_fixed_hmac_sha256(msg):
    """Generate HMAC SHA256 of a message with fixed key."""
    key = settings.HMAC_KEY
    hashed = hmac.new(key, msg, hashlib.sha256)
    return hashed.hexdigest()


def gen_hmac_sha1(key, msg):
    """Generate the HMAC SHA1 of a message."""
    hashed = hmac.new(key, msg, hashlib.sha1)
    return hashed.hexdigest()


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


def gen_sha256_files_n_dir(dirc):
    """Get the SHA256 hash of an entire directory."""
    sha2 = {}
    sha2_files = {}
    for root, _, files in os.walk(dirc):
        for fpath in [osp.join(root, f) for f in files]:
            sha256_hash = gen_sha256_file(fpath)
            sha2_files[fpath] = sha256_hash
    sha2['dir_sha256'] = gen_sha256_hash(json.dumps(sha2_files))
    sha2['files_sha256'] = sha2_files
    return sha2


def gen_hashes(locations):
    """Generate file and directory SHA256 hashes."""
    sha2_hashes = []
    for loc in locations:
        sha2 = gen_sha256_files_n_dir(loc)
        sha2_hashes.append(sha2)
    scan_hash = gen_sha256_hash(''.join(locations))
    hash_of_sha2 = gen_sha256_hash(json.dumps(sha2_hashes))
    return scan_hash, sha2_hashes, hash_of_sha2


def get_filename(path):
    """Get a filename from path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def year():
    """Get the current year."""
    now = datetime.datetime.now()
    return now.year


def random_string(size=6, chars=string.ascii_lowercase):
    """Random string generator (contains lowercase a-z and 0-9)."""
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punctuation_re.split(text.lower()):
        word = unicodedata.normalize('NFKD', word) \
            .encode('ascii', 'ignore') \
            .decode('utf-8')
        if word:
            result.append(word)
    return delim.join(result)


def js_escape(value):
    """Javascript XSS escapes."""
    return (value.replace('<', "\\u003c").
            replace('>', "\\u003e").
            replace('"', "\\u0022").
            replace("'", "\\u0027").
            replace("`", "\\u0060").
            replace("(", "\\u0028").
            replace(")", "\\u0029").
            replace("{", "\\u007b").
            replace("}", "\\u007d").
            replace("-", "\\u002d").
            replace("+", "\\u007d").
            replace("$", "\\u0024").
            replace("/", "\\u002f"))
