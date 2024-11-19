"""
Documentation Routes

This module handles documentation-related routes including API docs,
syntax guides, and examples.
"""
from flask import Blueprint, render_template
import markdown

bp = Blueprint('docs', __name__, url_prefix='/docs')

@bp.route('/')
def index():
    """Render main documentation page."""
    with open('docs/README.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=current_app.config['MARKDOWN_EXTENSIONS'])
    return render_template('markdown.html', content=content, title="Documentation")

@bp.route('/api')
def api_docs():
    """Render API documentation page."""
    with open('docs/api.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=current_app.config['MARKDOWN_EXTENSIONS'])
    return render_template('markdown.html', content=content, title="API Documentation")

@bp.route('/syntax')
def syntax():
    """Render syntax documentation page."""
    with open('docs/basic_syntax.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=current_app.config['MARKDOWN_EXTENSIONS'])
    return render_template('markdown.html', content=content, title="Basic Syntax")

@bp.route('/endpoints')
def endpoints():
    """Render endpoints documentation page."""
    with open('docs/endpoints.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=current_app.config['MARKDOWN_EXTENSIONS'])
    return render_template('markdown.html', content=content, title="API Endpoints")
