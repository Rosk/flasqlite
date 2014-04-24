# -*- coding: utf-8 -*-

"""
        --------------------------------------------------------------------
        ROSK Web App - Features:
        - sqlite db in schema.sql
        - userlogin / logout / Dublettenprüfung / password hash / Längenprüfung
        - Custom 404 pages
        - Sessions Variables
        - jsonify als Schnittstelle für ajax / python
        --------------------------------------------------------------------
"""

from app import app, ensure_dir

# Basic App Configuration
SECRET_KEY = 'lfhjk5h3l5jh345XD#*'
DATABASE = 'flaskSqlite.db'

# APP vars
app.title = "FlaskSqlite"
app.secret_key = SECRET_KEY
app.debug = True
app.database = DATABASE

# Bitte anpassen
app.port = 6061
app.home = "/home/rosk/Arbeitsfläche/"

uploadFolder = app.home + app.title + "Uploads/"

# App starten

# Upload-Verzeichnis existiert? sonst anlegen...
ensure_dir(uploadFolder)

# App starten
if __name__ == '__main__':
    app.run(debug=False, port=app.port)