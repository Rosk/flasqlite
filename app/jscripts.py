# -*- coding: utf-8 -*-
"""
    jQuery Scripte, die mit der App interagieren, werden hier referenziert...
"""

from app import app, jsonify, request
from colormath import *
from colormath.color_objects import XYZColor, RGBColor, CMYKColor, HSVColor, color_conversions, LabColor


@app.route('/_add_numbers')
def add_numbers():
    """Eine Besipielmethode, die über json mit jquery interagiert..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    res = a + b
    return jsonify(ergebnis=res)

