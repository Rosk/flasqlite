# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
from flask import Flask, render_template, g, flash, redirect, request, url_for, session, abort, jsonify, app
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from contextlib import closing
from functools import wraps


# Flask variables
app = Flask(__name__)
mail = Mail(app)
title = "FlaskSqlite"

# now import appMethods
from app import users, views, errorpage, jscripts

# define App Variables here
DATABASE = 'flaskSqlite.db'
MAIL_DEFAULT_SENDER = 'info@test.de'



# ----------------------------------------------------------------------------------------------------------------------
# Database Schema
def init_db():
    """ Die Datenbank wird nach einem vordefinierten Schema generiert.Die Methode kann aufgerufen werden und erzeugt die
    sqlite DB nach dem in der Schemadatei genannten Schema."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Database Connect, Request & Teardown
def connect_db():
    """ Helfermethoden um sich mit der Datenbank zu verbinden"""
    return sqlite3.connect(DATABASE)


@app.before_request
def before_request():
    """Stellt eine Verbindung zur Datenbank her"""
    g.db = connect_db()
    g.user = None
    g.debug = app.debug
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?', [session['user_id']], one=True)


@app.teardown_request
def teardown_request(exception):
    """Schliesst die Verbindung zur Datenbank."""
    if hasattr(g, 'db'):
        g.db.close()


# sqlite helper - usage: http://flask.pocoo.org/docs/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# Date & Time
# ----------------------------------------------------------------------------------------------------------------------
def format_datetime(timestamp):
    """Formatiert einen Timestring für die Ausgabe."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


# Decorators
# ----------------------------------------------------------------------------------------------------------------------
def login_erforderlich(f):
    """Der Decorator fragt ab ob der Benutzer eingeloggt ist, wenn nicht leitet er zum Login um"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Um diese Seite anschauen zu können, müssen Sie einen Account besitzen und eingeloggt sein.', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def admin_erforderlich(f):
    """Der Decorator fragt ab ob der Benutzerstatus kleiner zwei ist und leitet sonst zur Startseite"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user_status']:
            flash("Sie müssen Adminstrator sein um diese Seite betrachten zu können. Ihr Status: "
                  + str(session['user_status']))
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
# ----------------------------------------------------------------------------------------------------------------------


# Helfermethoden
# ----------------------------------------------------------------------------------------------------------------------
def ensure_dir(f):
    """Überprüft ob ein Verzeichnis für den Dateiupload existiert, erstellt es wenn nicht"""
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


# Routing - Register, Login Logout
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registeriert den user in die Datenbank."""
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'Sie müssen einen Benutzernamen eingeben'
        elif not request.form['email'] or '@' not in request.form['email']:
            error = 'Sie müssen eine valide Emailadresse angeben'
        elif sys.getsizeof(request.form['password'], default=0) < 64:
            error = 'Ihr Passwort ist zu kurz und sollte mindestens acht Zeichen haben.'
        elif not request.form['password']:
            error = 'Sie müssen ein Passwort angeben'
        elif not request.form['land']:
            error = 'Sie müssen ein Herkunftsland angeben'
        elif request.form['password'] != request.form['password2']:
            error = 'Die beiden Passwörter stimmen nicht berein'
        elif users.get_user_id(request.form['username']) is not None:
            error = 'Den Benutzernamen gibt es bereits in der Datenbank'

        # wenn es keine Fehler gibt, versuchen wir uns mit der DB zu verbinden
        else:
            db = connect_db()
            db.execute('''insert into user (
                user_name, user_email, user_pw_hash, user_land, user_points, user_status) values (?, ?, ?, ?, ?, ?)''',
                       [request.form['username'], request.form['email'],
                        generate_password_hash(request.form['password']),
                        request.form['land'], 0, 1])
            db.commit()
            flash('Sie sind jetzt erfolgreich registriert. Bitte loggen Sie sich mit Ihrem Account ein.', 'hinweis')
            return redirect(url_for('home'))

    if error is not None:
        # Utf-8 Sanitizer vor der Ausgabe
        error = error.decode('utf-8')
    return render_template('register.htm', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Loggt den user ein und weist die gewünschten Uservariablen den Sessionvariablen zu."""
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where user_name = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Ungültiger Benutzername - den Benutzer gibt es nicht in der Datenbank'
        elif not check_password_hash(user['user_pw_hash'], request.form['password']):
            error = 'Invalides Passwort - haben Sie sich vertippt? Groß/Kleinschreibung beachten!'
        else:
            flash('Sie sind jetzt eingeloggt. Herzlich Willkommen, ' + user['user_name'] + "!", 'hinweis')
            # Session Vars registrieren
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            session['user_status'] = user['user_status']
            session['user_points'] = user['user_points']
            return redirect(url_for('home'))

    # Bei Fehlern
    if error is not None:
        # Utf-8 Sanitizer vor der Ausgabe
        error = error.decode('utf-8')
        flash(error.encode('utf-8'), 'error')

    # Rückgabe
    return render_template('login.htm', error=error)


@app.route('/logout')
def logout():
    """Loggt den user aus und leert die zugewiesenen Sessionvariablen.
      Hier alle Variablen leeren, die im Login registriert wurden!"""
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_status', None)
    session.pop('user_points', None)
    # Danach zurück zur LoginSeite
    flash("Sie sind jetzt ausgeloggt. Auf Wiedersehen. Bis zum nächsten mal!", 'hinweis')
    return redirect(url_for('login'))


@app.route('/edituser/')
@app.route('/edituser/<userId>', methods=['GET', 'POST'])
def edit_user(userId):
    """Aktualisiert den bereits registrierten user in der Datenbank."""
    error = None
    session['user_edit'] = False
    uid = userId
    uname = request.form['user_name']
    uemail = request.form['user_email']
    uland = request.form['user_land']

    if not uid:
        error = "Sie sind nocht nicht registriert. Bitte registrieren sie sich."
    elif not uname:
        error = "Der Benutzername darf nicht leer sein"
    elif not uemail:
        error = "Die Emailadresse darf nicht leer sein"
    elif not uland:
        error = "Das Herkunftsland darf nicht leer sein"

    # Bei Fehlern
    if error is not None:
        error = error.decode('utf-8')
        flash(error.encode('utf-8'), 'error')
    else:
        db = connect_db()
        db.execute('UPDATE user SET user_name=?, user_email=?, user_land=? WHERE user_id=?',
                   [uname, uemail, uland, uid])
        db.commit()
        session['user_name'] = uname
        session['user_edit'] = True
        flash('Ihr Profil wurde aktualisiert', 'hinweis')
    return redirect(url_for('userinfo'))


# Falls die Datenbank noch nicht exisitiert muß sie einmal initialisert werden
# init_db()