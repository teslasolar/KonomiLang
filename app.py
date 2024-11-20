"""
Konomi Language Web Application

This module implements the main Flask application for the Konomi programming language,
providing both web interface and API endpoints.
"""
from flask import Flask, render_template, request, jsonify
from konomi.generators.examples import generate_components_example
from konomi.generators.svg.charts import ChartGenerator
from konomi.interpreter import Interpreter
from konomi.errors import KonomiError
from konomi.chained_programs import ProgramLibrary
from konomi.routes.core import setup_core_routes
from konomi.routes.chains import setup_chain_routes
from monitoring.api import monitor_api
from generation.functions import DocumentationGenerator
from konomi.generators.examples import generate_components_example
from konomi.generators.examples.svg_examples import (
    generate_example_card, generate_example_chart,
    generate_animated_loader, generate_animated_path,
    generate_pulse_animation
)
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

# Setup chain routes
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
@app.route('/docs/react-visualization')
@app.route('/examples/visualization')
def visualization_examples():
    """Render visualization examples page."""
    return render_template('visualization_examples.html')

@async_route
async def react_visualization_docs():
    """Render React visualization documentation page."""
    content, status = await load_markdown_file('docs/react-visualization.md', 'react-vis')
    return render_template('markdown.html', content=content, title="React Visualization"), status

    content, status = await load_markdown_file('docs/basic_syntax.md', 'syntax')
    return render_template('markdown.html', content=content, title="Basic Syntax"), status

@app.route('/examples')
def examples():
    """Render examples page."""
    return render_template('examples.html')

@app.route('/examples/html')
def example_html():
    """Render example HTML generation."""
    return generate_example_card()

@app.route('/examples/svg')
def example_svg():
    """Render example SVG generation."""
    return generate_example_chart(), 200, {'Content-Type': 'image/svg+xml'}
@app.route('/examples/svg/loader')
def example_svg_loader():
    """Render example animated SVG loader."""
    return generate_animated_loader(), 200, {'Content-Type': 'image/svg+xml'}

@app.route('/examples/svg/path')
def example_svg_path():
    """Render example SVG path animation."""
    return generate_animated_path(), 200, {'Content-Type': 'image/svg+xml'}

@app.route('/examples/svg/pulse')
def example_svg_pulse():
    """Render example SVG pulse animation."""
    return generate_pulse_animation(), 200, {'Content-Type': 'image/svg+xml'}
# Register modular routes
from konomi.web.routes.components import bp as components_bp
from konomi.web.routes.charts import bp as charts_bp

# Register documentation routes
from konomi.web.routes.docs import bp as docs_bp
app.register_blueprint(docs_bp)
app.register_blueprint(components_bp)
app.register_blueprint(charts_bp)

# Register API routes
from konomi.web.routes.execution import bp as execution_bp
app.register_blueprint(execution_bp)

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

from konomi.visualizers import run_all_benchmarks

@app.route('/api/v1/visualization/benchmark', methods=['POST'])
def benchmark_visualizations():
    """Run performance benchmarks for visualization methods."""
    try:
        iterations = request.json.get('iterations', 100)
        results = run_all_benchmarks(iterations)
        
        return jsonify({
            'success': True,
            'results': results,
            'unit': 'ms/iteration',
            'iterations': iterations
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)