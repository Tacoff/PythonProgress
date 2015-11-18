import sqlite3
from flask import Flask,request,session,g,redirect,url_for,\
abort,render_template,flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = '\x8aL\xef\xdf_Pu@G\x9e/\x15m9\xa9\xe9@#*\xc1\xfdn\xa6'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/flaskr.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique=True)
    password = db.Column(db.String(80), nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>'% self.username

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    title = db.Column(db.String(80), nullable = False)
    text = db.Column(db.String(200),nullable = False)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<entries %r>' % self.title

# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

# @app.before_request
# def before_request():
#     if not entries.query.all():
#         db.create_all()

# @app.teardown_request
# def teardown_request(exception):
#     g.db.close()

# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def show_entries():
    # cur = g.db.execute('select title, text from entries order by id desc')
    cur = Entries.query.order_by(-Entries.id)
    entrie = [dict(title=row.title, text=row.text) for row in cur]
    return render_template('show_entries.html', entries=entrie)


# @app.route('/registers')
# def regists_user():
#     return render_template('register.html')

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        usermatch = User.query.filter_by(username=request.form['username']).first()
        if usermatch:
            error = 'Username has been register'
        else:
            db.session.add(User(request.form['username'],request.form['password']))
            db.session.commit()
            flash('A new user was successfully registered')
    return render_template('register.html',error = error)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db.session.add(Entries(request.form['title'],request.form['text']))
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usermatch = User.query.filter_by(username=request.form['username']).first()
        if not usermatch:
            error = 'Invalid username'
        elif request.form['password'] != usermatch.password:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash(request.form['username']+' were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")