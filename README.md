flasqlite
=========

v.0.0.3

Eine rohe Skelett-WebApp auf Basis von Python Flask, Jinja und Sqlite als Ausgangspunkt für weitere Projekte.
Die App bietet ein einfaches Benutzer-LogIn mit Sessions mit einer kleine sqlite DB.

=========

## Flasqlite:

- sqlite DB Schema in app/schema.sql
- userlogin / logout / Dublettenprüfung / password hash / Längenprüfung
- Sessions Variablen
- jsonify als Schnittstelle für ajax / python


### Anwendung:
- mit Python starten, die Demo läuft auf Port 6061
- ggf. die db_init() Methode einmal starten um eine neue DB zu erstellen / die DB zu leeren
