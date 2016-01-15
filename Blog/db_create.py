#!/usr/bin/env python27
# -*- coding: utf8 -*-

from migrate.versioning import api
from fileconfig import SQLALCHEMY_DATABASE_URI
from fileconfig import SQLALCHEMY_MIGRATE_REPO
from fileconfig import SQLALCHEMY_TRACK_MODIFICATIONS
from appblog import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))