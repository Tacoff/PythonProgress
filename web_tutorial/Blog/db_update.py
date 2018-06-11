#!/usr/bin/env python27
# -*- coding: utf8 -*-


from migrate.versioning import api
from fileconfig import SQLALCHEMY_DATABASE_URI
from fileconfig import SQLALCHEMY_MIGRATE_REPO
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))