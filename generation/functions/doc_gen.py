"""
Documentation Generator for KonomiLang
Handles automatic generation of documentation, APIs, and directory structure
with caching and optimization features
"""
from typing import Dict, List, Optional, Any
import os
import json
import hashlib
import asyncio
import aiofiles
from pathlib import Path
from functools import lru_cache
import markdown
from concurrent.futures import ThreadPoolExecutor
from jinja2 import Environment, FileSystemLoader, select_autoescape

class DocumentationCache:
    def __init__(self):
        self.content_cache = {}
        self.hash_cache = {}
        self.markdown_cache = {}
        self.template_cache = {}
        self._executor = ThreadPoolExecutor(max_workers=4)

    def get_content(self, key: str) -> Optional[str]:
        return self.content_cache.get(key)

    def set_content(self, key: str, content: str):
        self.content_cache[key] = content
        self.hash_cache[key] = self._hash_content(content)

    def get_markdown(self, key: str) -> Optional[str]:
        return self.markdown_cache.get(key)

    def set_markdown(self, key: str, content: str):
        self.markdown_cache[key] = content

    def get_template(self, key: str) -> Optional[str]:
        return self.template_cache.get(key)

    def set_template(self, key: str, content: str):
        self.template_cache[key] = content
        self.hash_cache[key] = self._hash_content(content)

    def has_changed(self, key: str, content: str) -> bool:
        if key not in self.hash_cache:
            return True
        return self._hash_content(content) != self.hash_cache[key]

    @staticmethod
    def _hash_content(content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()

class DocumentationGenerator:
    def __init__(self, template_dir: str = "templates/docs"):
        self.default_params = {
            "format": "markdown",
            "include_examples": True,
            "include_schemas": True
        }
        self.cache = DocumentationCache()
        self.pending_writes = {}
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            enable_async=True
        )
        self._setup_template_filters()

    def _setup_template_filters(self):
        """Setup custom Jinja2 filters"""
        self.jinja_env.filters['code_highlight'] = self._highlight_code
        self.jinja_env.filters['markdown'] = self._render_markdown

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
        """Convert markdown to HTML"""
        return markdown.markdown(content, extensions=['fenced_code', 'codehilite'])

    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context"""
        try:
            template = self.jinja_env.get_template(template_name)
            return await template.render_async(**context)
        except Exception as e:
            raise Exception(f"Template rendering failed: {str(e)}")

    async def generate_api_docs(self, endpoints: List[Dict], output_path: str = "docs/api.md") -> str:
        """Generate API documentation using templates"""
        context = {
            "endpoints": endpoints,
            "title": "API Documentation",
            "description": "Complete API reference for the Konomi Language"
        }
        
        try:
            content = await self.render_template("api_docs.md.j2", context)
            
            if self.cache.has_changed('api_docs', content):
                self.cache.set_content('api_docs', content)
                self.pending_writes[output_path] = content
                await self._batch_write()
            
            return content
        except Exception as e:
            raise Exception(f"API documentation generation failed: {str(e)}")

    async def generate_component_docs(self, components: List[Dict], output_path: str = "docs/components.md") -> str:
        """Generate documentation for UI components using templates"""
        context = {
            "components": components,
            "title": "Component Documentation",
            "description": "Documentation for UI components"
        }
        
        try:
            content = await self.render_template("component_docs.md.j2", context)
            
            if self.cache.has_changed('component_docs', content):
                self.cache.set_content('component_docs', content)
                self.pending_writes[output_path] = content
                await self._batch_write()
            
            return content
        except Exception as e:
            raise Exception(f"Component documentation generation failed: {str(e)}")

    async def generate_syntax_docs(self, syntax_data: Dict, output_path: str = "docs/syntax.md") -> str:
        """Generate syntax documentation using templates"""
        context = {
            "syntax": syntax_data,
            "title": "Syntax Documentation",
            "description": "Complete syntax reference for the Konomi Language"
        }
        
        try:
            content = await self.render_template("syntax_docs.md.j2", context)
            
            if self.cache.has_changed('syntax_docs', content):
                self.cache.set_content('syntax_docs', content)
                self.pending_writes[output_path] = content
                await self._batch_write()
            
            return content
        except Exception as e:
            raise Exception(f"Syntax documentation generation failed: {str(e)}")

    async def _batch_write(self):
        """Batch write operations to reduce I/O"""
        for path, content in self.pending_writes.items():
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                async with aiofiles.open(path, 'w') as f:
                    await f.write(content)
            except Exception as e:
                print(f"Error writing to {path}: {str(e)}")
        self.pending_writes.clear()

    @lru_cache(maxsize=128)
    def discover_endpoints(self, app) -> List[Dict]:
        """Cache and discover all endpoints in a Flask application"""
        endpoints = []
        
        for rule in app.url_map.iter_rules():
            endpoint_data = {
                "path": rule.rule,
                "method": list(rule.methods - {"HEAD", "OPTIONS"})[0],
                "name": rule.endpoint,
                "description": app.view_functions[rule.endpoint].__doc__
            }
            
            if hasattr(app.view_functions[rule.endpoint], 'example'):
                endpoint_data['example'] = app.view_functions[rule.endpoint].example
            
            endpoints.append(endpoint_data)
        
        return endpoints

    def validate_template(self, template: Dict) -> bool:
        """Validate directory structure template"""
        def validate_node(node):
            if isinstance(node, dict):
                return all(validate_node(value) for value in node.values())
            return isinstance(node, (str, type(None)))
        
        return validate_node(template)

    def generate_directory_structure(self, template: Dict[str, any], base_path: str = ".") -> None:
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
