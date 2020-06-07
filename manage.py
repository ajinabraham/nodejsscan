#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Manage app."""
from flask_script import Manager

from flask_migrate import Migrate, MigrateCommand

from nodejsscan.app import app
from nodejsscan.models import db

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    app.run(
        threaded=True,
        debug=False,
        host='127.0.0.1',
        port=9090)


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
