# -*- coding: utf-8 -*-
from app import *
from functools import wraps
from datetime import datetime

# Decorators
# ----------------------------------------------------------------------------------------------------------------------
# TODO: Müssen Decorators in jedem .py - File vorkommen - oder kann man die nicht zentral ausgliedern?

def login_erforderlich(f):
    """Der Decorator fragt ab ob der Benutzer eingeloggt ist, wenn nicht leitet er zum login um"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_erforderlich(f):
    """Der Decorator fragt ab ob der Benutzerstatus kleiner zwei ist und leitet sonst zur Startseite"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user['user_status'] != 2:
            flash("Sie müssen Adminstrator sein um diese Seite betrachten zu können. Ihr Status: " + str(session['user_status']))
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
# ----------------------------------------------------------------------------------------------------------------------

# Standardabfragemethode zum Ausführen von Datenbankqueries
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# Usermethoden
def get_user_id(username):
    """Convenience method to look up the id for a username."""
    r = query_db('select user_id from user where user_name = ?',
                 [username], one=True)
    return r if r else None


def get_user_name(userid):
    """Convenience method to look up the name for a userid."""
    rv = query_db('select user_name from user where user_id = ?',
                  [userid], one=True)
    return rv[0] if rv else None


# Userrouting

@app.route('/userlist')
def user_list():
    """ Gibt eine Liste von allen Benutzern aus die registriert sind"""
    rv = query_db('select user_name from user')
    if rv is None:
        abort(404)
    return render_template('userlist.htm', users=query_db('''select user_name, user_id, user_email, user_land,
                                                        user_status, user_points from user order by user_points desc'''))


@app.route('/userinfo')
@login_erforderlich
def userinfo():
    sid = g.user['user_id']
    uname = g.user['user_name']
    uland = g.user['user_land']
    upoints = g.user['user_points']
    email = g.user['user_email']
    zeit = datetime.now()
    tag = zeit.day
    monat = zeit.month
    jahr = zeit.year
    return render_template('userinfo.htm', id=sid, zeit=zeit, tag=tag, jahr=jahr, monat=monat, name=uname, punkte=upoints, email=email)
