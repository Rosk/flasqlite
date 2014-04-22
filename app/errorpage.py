# -*- coding: utf-8 -*-

from app import app, render_template


@app.errorhandler(404)
def page_not_found(e):
    """Definiert eine eigene 404 Seite"""
    return render_template('404.htm'), 404