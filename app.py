"""
Konomi Language Web Application

This module implements the main Flask application for the Konomi programming language,
providing both web interface and API endpoints.
"""
from flask import Flask, render_template, request, jsonify
from konomi.interpreter import Interpreter
from konomi.errors import KonomiError
from konomi.chained_programs import ProgramLibrary
from konomi.routes.core import setup_core_routes
from konomi.routes.chains import setup_chain_routes
from monitoring.api import monitor_api
from generation.functions import DocumentationGenerator
import markdown
import os
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

# Initialize Flask application
app = Flask(__name__)

# Register monitoring API blueprint
app.register_blueprint(monitor_api, url_prefix='/api/v1/monitor')

# Initialize core components
interpreter = Interpreter()
program_library = ProgramLibrary(interpreter)
doc_generator = DocumentationGenerator()

# Setup modular routes
setup_core_routes(app, interpreter)
setup_chain_routes(app, program_library)

# Configure Markdown extensions
markdown_extensions = [
    'fenced_code',
    'codehilite',
    'tables',
    'attr_list'
]

def highlight_code(code, language='konomi'):
    """Syntax highlight code snippets."""
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style='monokai', cssclass='highlight')
        return highlight(code, lexer, formatter)
    except:
        return code

app.jinja_env.globals.update(highlight_code=highlight_code)

# Web interface routes
@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')

@app.route('/generation')
def generation():
    """Render code generation page."""
    return render_template('generation.html')

@app.route('/docs')
def docs():
    """Render documentation page."""
    # Auto-generate API documentation
    endpoints = doc_generator.discover_endpoints(app)
    doc_generator.generate_api_docs(endpoints, 'docs/api.md')
    
    with open('docs/README.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="Documentation")

@app.route('/docs/api')
def api_docs():
    """Render API documentation page."""
    with open('docs/api.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="API Documentation")

@app.route('/docs/endpoints')
def endpoints_docs():
    """Render endpoints documentation page."""
    with open('docs/endpoints.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="API Endpoints")

@app.route('/docs/syntax')
def syntax_docs():
    """Render syntax documentation page."""
    with open('docs/basic_syntax.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="Basic Syntax")

@app.route('/examples')
def examples():
    """Render examples page."""
    return render_template('examples.html')

# API Management endpoints
@app.route('/api/v1/docs/generate', methods=['POST'])
def generate_docs():
    """Generate documentation based on current API endpoints."""
    try:
        endpoints = doc_generator.discover_endpoints(app)
        doc_generator.generate_api_docs(endpoints)
        return jsonify({"success": True, "message": "Documentation generated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/v1/structure/generate', methods=['POST'])
def generate_structure():
    """Generate directory structure based on template."""
    try:
        template = request.json.get('template')
        if not template:
            return jsonify({"success": False, "error": "Template is required"}), 400
            
        if not doc_generator.validate_template(template):
            return jsonify({"success": False, "error": "Invalid template format"}), 400
            
        doc_generator.generate_directory_structure(template)
        return jsonify({"success": True, "message": "Directory structure generated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Web interface execute endpoint
@app.route('/execute', methods=['POST'])
def execute():
    """Execute Konomi code from web interface."""
    code = request.form.get('code', '')
    try:
        result = interpreter.execute(code)
        return jsonify({'success': True, 'result': result})
    except KonomiError as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
