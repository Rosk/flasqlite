# -*- coding: utf-8 -*-
from app import *
from functools import wraps

# Decorators
# ----------------------------------------------------------------------------------------------------------------------
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
        if session['user_status'] != 2:
            flash("Sie müssen Adminstrator sein um diese Seite betrachten zu können. Ihr Status: "
                  + str(session['user_status']))
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
# ----------------------------------------------------------------------------------------------------------------------

# sqlite helper - usage: http://flask.pocoo.org/docs/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

# ----------------------------------------------------------------------------------------------------------------------

@app.route('/')
def home():
    """Die Startseite der Applikation"""
    t = app.root_path
    return render_template('home.htm', rootpath=t)


@app.route('/admininfo')
@admin_erforderlich
def admininfo():
    return render_template('admininfo.htm')


@app.route('/about')
def about():
    """Registriert die Seite 'about' """

    if g.user:
        items = "eingeloggt als " + g.user['user_name']
    else:
        items = "Nicht eingeloggt"
    return render_template('about.htm', items=items)


@app.route('/imprint/')
def imprint():
    """Registriert die Seite 'Impressum' """
    if 'user_id' in session:
        loggedIn = "yes"
        sid = session['user_id']
    else:
        loggedIn = "no"
        sid = 0
    return render_template('imprint.htm', loggedin=loggedIn, id=sid)

