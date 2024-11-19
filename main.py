"""
Konomi Language Web Application Entry Point

This module serves as the entry point for the Konomi web application.
"""
from konomi.web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
