"""
Konomi Web Application

This module initializes and configures the Flask application for the Konomi programming language.
"""
from flask import Flask
from .config import configure_app

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../static')
    
    # Configure the application
    configure_app(app)
    
    # Import and register blueprints
    from .routes import docs, web, execution
    app.register_blueprint(docs.bp)
    app.register_blueprint(web.bp)
    app.register_blueprint(execution.bp)
    
    return app
