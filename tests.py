#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Basic tests."""
from datetime import datetime
import unittest

from nodejsscan.app import app
from nodejsscan.models import db
from nodejsscan import utils

from werkzeug.datastructures import FileStorage

INV_HASH = '4b3ce8526462b31de7cda339b121b10b299fcb42f4f5a7be48a08797b545f711'
VALID_HASH = 'a6c706242fe1040fb94b53625c98b7d36c94cfffd3f40981faf0d04e1796db1f'


def _tim():
    """Patch timestamp for test."""
    return datetime.now()


utils.get_timestamp = _tim


class Tests(unittest.TestCase):
    """Tests."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.app_context().push()
        db.create_all()
        self.app = app.test_client()
        self.assertEqual(app.debug, True)

    def tearDown(self):
        """Executed after each test."""
        pass

    def test_index(self):
        """Index."""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_scans(self):
        """Scans."""
        response = self.app.get('/scans', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_hash_scan(self):
        """Scan with invalid hash."""
        response = self.app.get('/scan/blaa', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_no_hash_scan(self):
        """Scan with non existing hash."""
        response = self.app.get(
            f'/scan/{INV_HASH}',
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_json, True)
        self.assertEqual(response.json, {
            'message': 'Scan hash not found',
            'status': 'failed'})

    def test_invalid_hash_search(self):
        """Search with non existing hash."""
        dat = {
            'q': 'js',
            'scan_hash': INV_HASH,
        }
        response = self.app.post(
            '/search',
            data=dat,
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_json, True)
        self.assertEqual(response.json, {
            'message': 'Scan hash not found',
            'status': 'failed'})

    def test_a_scan(self):
        """Test file upload and scan."""
        testzip = FileStorage(
            stream=open('static/tests/test_assets.zip', 'rb'),
            filename='test_assets.zip',
            content_type='application/zip',
        )
        response = self.app.post(
            '/upload/',
            content_type='multipart/form-data',
            data={'file': testzip},
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_json, True)
        self.assertEqual(response.json, {
            'status': 'success',
            'url': f'scan/{VALID_HASH}'})

    def test_search(self):
        """Test search."""
        test_str = b'test_assets/js/express_bodyparser_dos.js'
        dat = {
            'q': 'body',
            'scan_hash': VALID_HASH,
        }
        response = self.app.post(
            '/search',
            data=dat,
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_json, False)
        self.assertEqual(test_str in response.data, True)

    def test_view(self):
        """Test view file."""
        vfile = 'test_assets/js/express_bodyparser_dos.js'
        dat = {
            'path': f'{VALID_HASH}/{vfile}',
            'scan_hash': VALID_HASH,
        }
        response = self.app.post(
            '/view_file',
            data=dat,
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_json, True)
        self.assertEqual('contents' in response.json, True)

    def test_view_path_traversal(self):
        """Attempt path traversal."""
        dat = {
            'path': '../../../../etc/passwd',
            'scan_hash': VALID_HASH,
        }
        response = self.app.post(
            '/view_file',
            data=dat,
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_json, True)
        self.assertEqual(response.json, {
            'contents': 'Path Traversal Detected!',
            'status': 'failed'})

    def test_view_scan(self):
        """Scan with invalid hash."""
        response = self.app.get(f'/scan/{VALID_HASH}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_z_delete_scan(self):
        """Test delete scan."""
        dat = {
            'scan_hash': VALID_HASH,
        }
        response = self.app.post(
            '/delete_scan',
            data=dat,
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_json, True)
        self.assertEqual(response.json, {
            'status': 'ok'})


if __name__ == '__main__':
    unittest.main()
