"""
Documentation Routes

This module handles documentation-related routes including API docs,
syntax guides, and examples.
"""
from flask import Blueprint, render_template, current_app
import markdown
import os
import logging
import aiofiles
from pathlib import Path
from generation.functions import DocumentationGenerator
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)
bp = Blueprint('docs', __name__, url_prefix='/docs')

# Initialize documentation generator
doc_generator = DocumentationGenerator()

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

async def load_markdown_file(filepath: str, cache_key: str) -> tuple[str, int]:
    """Load and process markdown file with error handling."""
    try:
        if not os.path.exists(filepath):
            logger.warning(f"Documentation file not found: {filepath}")
            content = "# Documentation Not Found\n\nThe requested documentation is currently unavailable."
            return await doc_generator.process_markdown(content, 'default'), 404

        async with aiofiles.open(filepath, 'r') as f:
            content = await f.read()
            processed_content = await doc_generator.process_markdown(
                content,
                cache_key
            )
            return processed_content, 200
    except Exception as e:
        logger.error(f"Error loading markdown file {filepath}: {str(e)}")
        return f"Error loading documentation: {str(e)}", 500

@bp.route('/')
@async_route
async def index():
    """Render main documentation page."""
    content, status = await load_markdown_file('docs/README.md', 'readme')
    return render_template('markdown.html', content=content, title="Documentation"), status

@bp.route('/api')
@async_route
async def api_docs():
    """Render API documentation page."""
    try:
        # Generate fresh API documentation
        endpoints = doc_generator.discover_endpoints(current_app)
        await doc_generator.generate_api_docs(endpoints, 'docs/api.md')
        content, status = await load_markdown_file('docs/api.md', 'api')
        return render_template('markdown.html', content=content, title="API Documentation"), status
    except Exception as e:
        logger.error(f"Error in api_docs: {str(e)}")
        return render_template('markdown.html', 
                             content=f"Error generating API documentation: {str(e)}", 
                             title="Error"), 500

@bp.route('/syntax')
@async_route
async def syntax():
    """Render syntax documentation page."""
    content, status = await load_markdown_file('docs/basic_syntax.md', 'syntax')
    return render_template('markdown.html', content=content, title="Basic Syntax"), status

@bp.route('/endpoints')
@async_route
async def endpoints():
    """Render endpoints documentation page."""
    content, status = await load_markdown_file('docs/endpoints.md', 'endpoints')
    return render_template('markdown.html', content=content, title="API Endpoints"), status
