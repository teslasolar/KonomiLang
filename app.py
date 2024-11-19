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
import logging
import aiofiles
from pathlib import Path
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
import asyncio
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Configure Flask application
app.config['MARKDOWN_EXTENSIONS'] = [
    'fenced_code',
    'codehilite',
    'tables',
    'attr_list'
]

# Register monitoring API blueprint
app.register_blueprint(monitor_api, url_prefix='/api/v1/monitor')

# Initialize core components
interpreter = Interpreter()
program_library = ProgramLibrary(interpreter)
doc_generator = DocumentationGenerator()

# Setup modular routes
setup_core_routes(app, interpreter)
setup_chain_routes(app, program_library)

# Ensure docs directory exists
docs_dir = Path('docs')
docs_dir.mkdir(exist_ok=True)

# Default documentation content
DEFAULT_DOC_CONTENT = """
# Documentation Not Found

The requested documentation is currently being generated or is not available.
Please try again in a few moments or contact the system administrator.

## Available Documentation Sections:
- [API Documentation](/docs/api)
- [Endpoints Documentation](/docs/endpoints)
- [Basic Syntax](/docs/syntax)
"""

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(f(*args, **kwargs))
        except Exception as e:
            logger.error(f"Error in async route {f.__name__}: {str(e)}")
            return render_template(
                'markdown.html',
                content=f"Error: {str(e)}",
                title="Error"
            ), 500
    return wrapper

def highlight_code(code, language='konomi'):
    """Syntax highlight code snippets."""
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style='monokai', cssclass='highlight')
        return highlight(code, lexer, formatter)
    except Exception as e:
        logger.warning(f"Failed to highlight code: {str(e)}")
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

async def load_markdown_file(filepath: str, cache_key: str) -> tuple[str, int]:
    """Load and process markdown file with error handling."""
    try:
        if not os.path.exists(filepath):
            logger.warning(f"Documentation file not found: {filepath}")
            return await doc_generator.process_markdown(DEFAULT_DOC_CONTENT, 'default'), 404

        async with aiofiles.open(filepath, 'r') as f:
            content = await f.read()
            processed_content = await doc_generator.process_markdown(content, cache_key)
            return processed_content, 200
    except Exception as e:
        logger.error(f"Error loading markdown file {filepath}: {str(e)}")
        return f"Error loading documentation: {str(e)}", 500

@app.route('/docs')
@async_route
async def docs():
    """Render documentation page."""
    try:
        # Auto-generate API documentation
        endpoints = doc_generator.discover_endpoints(app)
        await doc_generator.generate_api_docs(endpoints, 'docs/api.md')
        
        content, status = await load_markdown_file('docs/README.md', 'readme')
        return render_template('markdown.html', content=content, title="Documentation"), status
    except Exception as e:
        logger.error(f"Error in docs route: {str(e)}")
        return render_template(
            'markdown.html',
            content=await doc_generator.process_markdown(DEFAULT_DOC_CONTENT, 'default'),
            title="Documentation"
        ), 500

@app.route('/docs/api')
@async_route
async def api_docs():
    """Render API documentation page."""
    content, status = await load_markdown_file('docs/api.md', 'api')
    return render_template('markdown.html', content=content, title="API Documentation"), status

@app.route('/docs/endpoints')
@async_route
async def endpoints_docs():
    """Render endpoints documentation page."""
    content, status = await load_markdown_file('docs/endpoints.md', 'endpoints')
    return render_template('markdown.html', content=content, title="API Endpoints"), status

@app.route('/docs/syntax')
@async_route
async def syntax_docs():
    """Render syntax documentation page."""
    content, status = await load_markdown_file('docs/basic_syntax.md', 'syntax')
    return render_template('markdown.html', content=content, title="Basic Syntax"), status

@app.route('/examples')
def examples():
    """Render examples page."""
    return render_template('examples.html')

# API Management endpoints
@app.route('/api/v1/docs/generate', methods=['POST'])
@async_route
async def generate_docs():
    """Generate documentation based on current API endpoints."""
    try:
        endpoints = doc_generator.discover_endpoints(app)
        await doc_generator.generate_api_docs(endpoints)
        return jsonify({"success": True, "message": "Documentation generated successfully"})
    except Exception as e:
        logger.error(f"Error generating documentation: {str(e)}")
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
        logger.error(f"Error generating directory structure: {str(e)}")
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
        logger.error(f"Error executing code: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)