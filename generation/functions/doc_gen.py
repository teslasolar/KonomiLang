"""
Documentation Generator for KonomiLang
Handles automatic generation of documentation, APIs, and directory structure
with caching and optimization features
"""
from typing import Dict, List, Optional, Any, Set
import os
import json
import hashlib
import asyncio
import aiofiles
from pathlib import Path
from functools import lru_cache
import markdown
from concurrent.futures import ThreadPoolExecutor
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import time
import inspect
from flask import current_app
import re
import logging

logger = logging.getLogger(__name__)

class DocumentationCache:
    def __init__(self):
        self.content_cache = {}
        self.hash_cache = {}
        self.markdown_cache = {}
        self.template_cache = {}
        self.template_versions = {}
        self.template_dependencies = {}
        self._executor = ThreadPoolExecutor(max_workers=4)
        self.last_render_time = {}

    def get_content(self, key: str) -> Optional[str]:
        return self.content_cache.get(key)

    def set_content(self, key: str, content: str):
        self.content_cache[key] = content
        self.hash_cache[key] = self._hash_content(content)

    def get_markdown(self, key: str) -> Optional[str]:
        return self.markdown_cache.get(key)

    def set_markdown(self, key: str, content: str):
        self.markdown_cache[key] = content

    def get_template(self, key: str) -> Optional[tuple[str, int]]:
        if key in self.template_cache:
            return self.template_cache[key], self.template_versions.get(key, 1)
        return None

    def set_template(self, key: str, content: str, dependencies: Optional[Set[str]] = None):
        self.template_cache[key] = content
        self.hash_cache[key] = self._hash_content(content)
        current_version = self.template_versions.get(key, 0)
        self.template_versions[key] = current_version + 1
        if dependencies:
            self.template_dependencies[key] = dependencies

    def invalidate_dependent_templates(self, template_key: str):
        for key, deps in self.template_dependencies.items():
            if template_key in deps:
                if key in self.template_versions:
                    self.template_versions[key] += 1

    def should_rerender(self, template_key: str, min_interval: float = 5.0) -> bool:
        current_time = time.time()
        last_time = self.last_render_time.get(template_key, 0)
        
        if current_time - last_time < min_interval:
            return False
        
        if template_key in self.template_dependencies:
            for dep in self.template_dependencies[template_key]:
                if self.has_changed(dep, self.template_cache.get(dep, '')):
                    return True
        
        return True

    def update_render_time(self, template_key: str):
        self.last_render_time[template_key] = time.time()

    def has_changed(self, key: str, content: str) -> bool:
        if key not in self.hash_cache:
            return True
        return self._hash_content(content) != self.hash_cache[key]

    @staticmethod
    def _hash_content(content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()

class EndpointMetadata:
    def __init__(self, func, rule, methods):
        self.func = func
        self.rule = rule
        self.methods = methods
        self.docstring = inspect.getdoc(func) or ""
        self.parameters = self._extract_parameters()
        self.response_schema = self._extract_response_schema()
        self.example = self._extract_example()

    def _extract_parameters(self) -> Dict:
        """Extract parameters from function signature and docstring"""
        params = {}
        signature = inspect.signature(self.func)
        
        for name, param in signature.parameters.items():
            if name not in ['self', 'args', 'kwargs']:
                param_info = {
                    'type': str(param.annotation) if param.annotation != inspect._empty else 'any',
                    'default': None if param.default == inspect._empty else param.default,
                    'required': param.default == inspect._empty
                }
                params[name] = param_info
        
        return params

    def _extract_response_schema(self) -> Dict:
        """Extract response schema from docstring or return annotations"""
        schema = {'type': 'object', 'properties': {}}
        
        # Try to get from return annotation
        return_annotation = inspect.signature(self.func).return_annotation
        if return_annotation != inspect._empty:
            schema['return_type'] = str(return_annotation)
        
        # Look for response schema in docstring
        if 'Returns:' in self.docstring:
            returns_section = self.docstring.split('Returns:')[1].split('\n')[0]
            schema['description'] = returns_section.strip()
        
        return schema

    def _extract_example(self) -> Optional[Dict]:
        """Extract example usage from docstring"""
        if 'Example:' in self.docstring:
            example_section = self.docstring.split('Example:')[1].split('\n\n')[0]
            return {
                'description': 'Example usage',
                'code': example_section.strip()
            }
        return None

    def to_dict(self) -> Dict:
        """Convert endpoint metadata to dictionary"""
        return {
            'path': self.rule,
            'methods': list(self.methods - {'HEAD', 'OPTIONS'}),
            'description': self.docstring,
            'parameters': self.parameters,
            'response_schema': self.response_schema,
            'example': self.example
        }

class DocumentationGenerator:
    def __init__(self, template_dir: str = "templates/docs"):
        self.default_params = {
            "format": "markdown",
            "include_examples": True,
            "include_schemas": True
        }
        self.cache = DocumentationCache()
        self.pending_writes = {}
        self.template_dir = template_dir
        self.jinja_env = self._setup_jinja_env()
        self.custom_formats = {}
        self._setup_template_filters()
        self.markdown_extensions = [
            'fenced_code',
            'codehilite',
            'tables',
            'attr_list',
            'toc'
        ]

    def _setup_jinja_env(self) -> Environment:
        """Setup Jinja environment with inheritance support"""
        env = Environment(
            loader=FileSystemLoader([self.template_dir, "templates"]),
            autoescape=select_autoescape(['html', 'xml']),
            enable_async=True,
            cache_size=100,
            auto_reload=True
        )
        return env

    def _setup_template_filters(self):
        """Setup custom Jinja2 filters"""
        self.jinja_env.filters['code_highlight'] = self._highlight_code
        self.jinja_env.filters['markdown'] = self._render_markdown
        self.jinja_env.filters['format_date'] = lambda d: d.strftime('%Y-%m-%d %H:%M:%S')

    def _highlight_code(self, code: str, language: str = 'python') -> str:
        """Syntax highlighting filter for code blocks"""
        try:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import HtmlFormatter
            
            lexer = get_lexer_by_name(language)
            formatter = HtmlFormatter(style='monokai')
            return highlight(code, lexer, formatter)
        except Exception:
            return code

    def _render_markdown(self, content: str) -> str:
        """Convert markdown to HTML with extended features"""
        return markdown.markdown(
            content,
            extensions=self.markdown_extensions,
            output_format='html5'
        )

    def discover_endpoints(self, app) -> List[Dict]:
        """Discover and analyze all endpoints in a Flask application"""
        endpoints = []
        
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':  # Skip static file serving
                view_func = app.view_functions[rule.endpoint]
                metadata = EndpointMetadata(view_func, rule.rule, rule.methods)
                endpoints.append(metadata.to_dict())
        
        return endpoints

    async def generate_api_docs(self, endpoints: List[Dict], output_path: str = "docs/api.md") -> str:
        """Generate API documentation using templates with enhanced metadata"""
        # Group endpoints by their base path
        grouped_endpoints = {}
        for endpoint in endpoints:
            base_path = endpoint['path'].split('/')[1]
            if base_path not in grouped_endpoints:
                grouped_endpoints[base_path] = []
            grouped_endpoints[base_path].append(endpoint)

        context = {
            "groups": grouped_endpoints,
            "title": "API Documentation",
            "description": "Complete API reference for the Konomi Language",
            "current_version": "1.0"
        }
        
        try:
            content = await self.render_template(
                "api_docs.md.j2",
                context,
                cache_key='api_docs'
            )
            
            if self.cache.has_changed('api_docs', content):
                self.cache.set_content('api_docs', content)
                self.pending_writes[output_path] = content
                await self._batch_write()
            
            return content
        except Exception as e:
            raise Exception(f"API documentation generation failed: {str(e)}")

    async def process_markdown(self, content: str, cache_key: str) -> str:
        """
        Process markdown content with caching support and proper HTML formatting
        
        Args:
            content: Raw markdown content to process
            cache_key: Cache key for storing processed content
            
        Returns:
            str: Processed HTML content
        """
        try:
            if cached_content := self.cache.get_markdown(cache_key):
                return cached_content
            
            loop = asyncio.get_event_loop()
            processed_content = await loop.run_in_executor(
                self.cache._executor,
                lambda: markdown.markdown(
                    content,
                    extensions=self.markdown_extensions,
                    output_format='html5'
                )
            )
            
            self.cache.set_markdown(cache_key, processed_content)
            return processed_content
        except Exception as e:
            logger.error(f"Failed to process markdown: {str(e)}")
            raise

    def generate_directory_structure(self, template: Dict[str, Any], base_path: str = ".") -> bool:
        """
        Generate directory structure based on template with improved error handling
        
        Args:
            template: Dictionary containing directory structure
            base_path: Base path for structure creation
            
        Returns:
            bool: True if structure was created successfully, False otherwise
        """
        base = Path(base_path)
        
        def create_structure(structure: Dict, current_path: Path) -> bool:
            try:
                for name, content in structure.items():
                    path = current_path / name
                    
                    if isinstance(content, dict):
                        path.mkdir(exist_ok=True, parents=True)
                        if not create_structure(content, path):
                            return False
                    else:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        if content is not None:
                            path.write_text(content)
                        else:
                            path.touch()  # Create empty file
                return True
            except Exception as e:
                logger.error(f"Error creating structure at {current_path}: {str(e)}")
                return False

        if not self.validate_template(template):
            logger.error("Invalid template format")
            return False
            
        return create_structure(template, base)

    async def _batch_write(self) -> None:
        """Batch write operations to reduce I/O with proper async handling"""
        async with asyncio.Lock():
            for path, content in self.pending_writes.items():
                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    async with aiofiles.open(path, 'w') as f:
                        await f.write(content)
                except Exception as e:
                    logger.error(f"Error writing to {path}: {str(e)}")
            self.pending_writes.clear()

    async def render_template(self, template_name: str, context: Dict[str, Any], cache_key: Optional[str] = None) -> str:
        """Render a template with caching and dependency tracking"""
        try:
            if cache_key and not self.cache.should_rerender(cache_key):
                cached_template = self.cache.get_template(cache_key)
                if cached_template:
                    content, version = cached_template
                    return content

            template = self.jinja_env.get_template(template_name)
            
            # Track template dependencies using template.filename
            dependencies = {template_name}
            template_stack = [template]
            
            # Traverse up the template hierarchy
            while template_stack:
                current_template = template_stack.pop()
                if hasattr(current_template, 'filename'):
                    template_filename = current_template.filename
                    if template_filename:
                        dependencies.add(os.path.basename(template_filename))
                # Check for extends and include tags in the template source
                if hasattr(current_template, 'blocks'):
                    for block in current_template.blocks.values():
                        if isinstance(block, Template) and hasattr(block, 'filename'):
                            block_filename = block.filename
                            if block_filename:
                                dependencies.add(os.path.basename(block_filename))

            content = await template.render_async(**context)
            
            if cache_key:
                self.cache.set_template(cache_key, content, dependencies)
                self.cache.update_render_time(cache_key)
            
            return content
        except Exception as e:
            raise Exception(f"Template rendering failed: {str(e)}")

    async def generate_error_docs(self, error_definitions: List[Dict], output_path: str = "docs/errors.md") -> str:
        """Generate error documentation using templates"""
        context = {
            "errors": error_definitions,
            "title": "Error Reference",
            "description": "Complete error code reference"
        }
        
        try:
            content = await self.render_template(
                "error_docs.md.j2",
                context,
                cache_key='error_docs'
            )
            
            if self.cache.has_changed('error_docs', content):
                self.cache.set_content('error_docs', content)
                self.pending_writes[output_path] = content
                await self._batch_write()
            
            return content
        except Exception as e:
            raise Exception(f"Error documentation generation failed: {str(e)}")

    def validate_template(self, template: Dict) -> bool:
        """Validate directory structure template"""
        def validate_node(node):
            if isinstance(node, dict):
                return all(validate_node(value) for value in node.values())
            return isinstance(node, (str, type(None)))
        
        return validate_node(template)

    def generate_directory_structure(self, template: Dict[str, Any], base_path: str = ".") -> None:
        """Generate directory structure based on template with error handling"""
        base = Path(base_path)
        
        def create_structure(structure: Dict, current_path: Path):
            for name, content in structure.items():
                path = current_path / name
                
                try:
                    if isinstance(content, dict):
                        path.mkdir(exist_ok=True)
                        create_structure(content, path)
                    else:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        if content is not None:
                            with open(path, 'w') as f:
                                f.write(content)
                except Exception as e:
                    print(f"Error creating {path}: {str(e)}")
        
        if self.validate_template(template):
            create_structure(template, base)
        else:
            raise ValueError("Invalid template format")