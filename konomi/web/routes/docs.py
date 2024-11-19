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

logger = logging.getLogger(__name__)
bp = Blueprint('docs', __name__, url_prefix='/docs')

# Initialize documentation generator
doc_generator = DocumentationGenerator()

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
                cache_key,
                extensions=current_app.config.get('MARKDOWN_EXTENSIONS', [])
            )
            return processed_content, 200
    except Exception as e:
        logger.error(f"Error loading markdown file {filepath}: {str(e)}")
        return f"Error loading documentation: {str(e)}", 500

@bp.route('/')
async def index():
    """Render main documentation page."""
    content, status = await load_markdown_file('docs/README.md', 'readme')
    return render_template('markdown.html', content=content, title="Documentation"), status

@bp.route('/api')
async def api_docs():
    """Render API documentation page."""
    # Generate fresh API documentation
    try:
        endpoints = doc_generator.discover_endpoints(current_app)
        await doc_generator.generate_api_docs(endpoints, 'docs/api.md')
    except Exception as e:
        logger.error(f"Error generating API docs: {str(e)}")

    content, status = await load_markdown_file('docs/api.md', 'api')
    return render_template('markdown.html', content=content, title="API Documentation"), status

@bp.route('/syntax')
async def syntax():
    """Render syntax documentation page."""
    content, status = await load_markdown_file('docs/basic_syntax.md', 'syntax')
    return render_template('markdown.html', content=content, title="Basic Syntax"), status

@bp.route('/endpoints')
async def endpoints():
    """Render endpoints documentation page."""
    content, status = await load_markdown_file('docs/endpoints.md', 'endpoints')
    return render_template('markdown.html', content=content, title="API Endpoints"), status
