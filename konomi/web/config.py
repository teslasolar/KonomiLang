"""
Application Configuration

This module handles the Flask application configuration settings.
"""
import os
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from monitoring.api import monitor_api

def highlight_code(code, language='konomi'):
    """Syntax highlight code snippets."""
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style='monokai', cssclass='highlight')
        return highlight(code, lexer, formatter)
    except:
        return code

def configure_app(app):
    """Configure Flask application settings and extensions."""
    # Register monitoring API blueprint
    app.register_blueprint(monitor_api, url_prefix='/api/v1/monitor')
    
    # Configure Markdown extensions
    app.config['MARKDOWN_EXTENSIONS'] = [
        'fenced_code',
        'codehilite',
        'tables',
        'attr_list'
    ]
    
    # Add template globals
    app.jinja_env.globals.update(highlight_code=highlight_code)
    
    # Configure application
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
    )
