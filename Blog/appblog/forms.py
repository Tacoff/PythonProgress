# -*- coding: utf8 -*-

from flask_wtf import Form
from wtforms import TextField, BooleanField,TextAreaField
from wtforms.validators import DataRequired,DataLength

# from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
# from flask.ext.wtf import Required, Length
 
# class EditForm(Form):
#     nickname = TextField('nickname', validators = [Required()])
#     about_me = TextAreaField('about_me', validators = [DataLength(min = 0, max = 140)])
 
class LoginForm(Form):
    openid = TextField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)