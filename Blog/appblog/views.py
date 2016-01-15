# -*- coding: utf8 -*-

# from appblog import app,lm
# from flask import render_template,flash,redirect
# from forms import LoginForm

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appblog import app, db, lm, oid
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN
from datetime import datetime

# @app.route('/')
# @app.route('/index')
# def index():
#     user = { 'nickname': 'Miguel' } # fake user
#     posts = [ # fake array of posts
#         {
#             'author': { 'nickname': 'John' },
#             'body': 'Beautiful day in Portland!'
#         },
#         {
#             'author': { 'nickname': 'Susan' },
#             'body': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template("index.html",
#         title = 'Home',
#         user = user,
#         posts = posts)

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)

# @app.route("/login",methods = ['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#         return redirect('/index')
#     return render_template('login.html',title = 'Sign In', form = form)

# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#         return redirect('/index')
#     return render_template('login.html',
#         title = 'Sign In',
#         form = form,
#         providers = app.config['OPENID_PROVIDERS'])

#http://openid.org.cn/home
#http://tacoff.openid.org.cn/
#tacoff
#lhzhsbYY443484

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    #flask_login 0.3之后将authenticated从函数更改为属性
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('不存在用户：' + nickname + '！')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html',
        user = user,
        posts = posts)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()