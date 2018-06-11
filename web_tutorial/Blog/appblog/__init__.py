# -*- coding: utf8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_openid import OpenID
from fileconfig import basedir
 
app = Flask(__name__)
app.config.from_object("fileconfig")
db = SQLAlchemy(app)
lm = LoginManager()
lm.setup_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))
lm.login_view = 'login'

from appblog import views,models

