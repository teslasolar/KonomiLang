"""
Web Interface Routes

This module handles web interface routes including the REPL interface
and example pages.
"""
from flask import Blueprint, render_template

bp = Blueprint('web', __name__)

@bp.route('/')
def index():
    """Render main page with REPL interface."""
    return render_template('index.html')

@bp.route('/examples')
def examples():
    """Render examples page."""
    return render_template('examples.html')

@bp.route('/generation')
def generation():
    """Render code generation page."""
    return render_template('generation.html')
