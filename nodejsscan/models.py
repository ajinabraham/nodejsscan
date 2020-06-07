#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Database Model."""
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class ScanResults(db.Model):
    __tablename__ = 'nodejsscan_results'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    scan_file = db.Column(db.String)
    scan_hash = db.Column(db.String(64), unique=True)
    location = db.Column(db.String)
    nodejs = db.Column(JSON)
    templates = db.Column(JSON)
    files = db.Column(JSON)
    false_positive = db.Column(JSON)
    not_applicable = db.Column(JSON)
    timestamp = db.Column(db.DateTime())

    def __init__(self,
                 scan_file,
                 scan_hash,
                 location,
                 nodejs,
                 templates,
                 files,
                 false_positive,
                 not_applicable,
                 timestamp):
        self.scan_file = scan_file
        self.scan_hash = scan_hash
        self.location = location
        self.nodejs = nodejs
        self.templates = templates
        self.files = files
        self.false_positive = false_positive
        self.not_applicable = not_applicable
        self.timestamp = timestamp

    def __repr__(self):
        """Repr."""
        return '<id {}>'.format(self.id)
