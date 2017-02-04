#!/usr/bin/env python
# -*- coding: utf_8 -*-
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSON
from database import Base


class Results(Base):
    """For Scan Results"""
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    scan_hash = Column(String(64), unique=True)
    locations = Column(JSON)
    sha2_hashes = Column(JSON)
    hash_of_sha2 = Column(String(64))
    sec_issues = Column(JSON)
    good_finding = Column(JSON)
    missing_sec_header = Column(JSON)
    files = Column(JSON)
    total_count = Column(JSON)
    vuln_count = Column(JSON)
    resolved = Column(JSON)
    invalid = Column(JSON)
    timestamp = Column(DateTime())

    def __init__(self, *args):
        """init"""
        self.scan_hash = args[0]
        self.locations = args[1]
        self.sha2_hashes = args[2]
        self.hash_of_sha2 = args[3]
        self.sec_issues = args[4]
        self.good_finding = args[5]
        self.missing_sec_header = args[6]
        self.files = args[7]
        self.total_count = args[8]
        self.vuln_count = args[9]
        self.resolved = args[10]
        self.invalid = args[11]
        self.timestamp = args[12]

    def __repr__(self):
        """repr"""
        return '<Results %r>' % self.scan_hash
