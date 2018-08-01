#!/usr/bin/env python
# -*- coding: utf_8 -*-
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

import core.settings as settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Results(Base):
    """For Scan Results"""
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    scan_file = Column(String)
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
        self.scan_file = args[0]
        self.scan_hash = args[1]
        self.locations = args[2]
        self.sha2_hashes = args[3]
        self.hash_of_sha2 = args[4]
        self.sec_issues = args[5]
        self.good_finding = args[6]
        self.missing_sec_header = args[7]
        self.files = args[8]
        self.total_count = args[9]
        self.vuln_count = args[10]
        self.resolved = args[11]
        self.invalid = args[12]
        self.timestamp = args[13]

    def __repr__(self):
        """repr"""
        return '<Results %r>' % self.scan_hash

Base.metadata.create_all(bind=engine)
print("[INFO] Table entries created!")
