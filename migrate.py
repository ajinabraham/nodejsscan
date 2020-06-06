#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Database Migration."""
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

import nodejsscan.settings as settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class ScanResults(Base):
    """For Scan Results."""

    __tablename__ = 'nodejsscan_results'
    id = Column(Integer, primary_key=True)  # noqa: A003
    scan_file = Column(String)
    scan_hash = Column(String(64), unique=True)
    location = Column(JSON)
    nodejs = Column(JSON)
    templates = Column(JSON)
    files = Column(JSON)
    severity = Column(JSON)
    false_positive = Column(JSON)
    not_applicable = Column(JSON)
    timestamp = Column(DateTime())

    def __init__(self, *args):
        """Init."""
        self.scan_file = args[0]
        self.scan_hash = args[1]
        self.location = args[2]
        self.nodejs = args[3]
        self.templates = args[4]
        self.files = args[5]
        self.false_positive = args[6]
        self.not_applicable = args[7]
        self.timestamp = args[8]

    def __repr__(self):
        """Repr."""
        return '<ScanResults %r>' % self.scan_hash


def main():
    """Migrate DB."""
    Base.metadata.create_all(bind=engine)
    print('[INFO] Table entries created!')


if __name__ == '__main__':
    main()
