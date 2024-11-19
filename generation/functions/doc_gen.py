"""
Documentation Generator for KonomiLang
Handles automatic generation of documentation, APIs, and directory structure
with caching and optimization features
"""
from typing import Dict, List, Optional
import os
import json
import hashlib
import asyncio
import aiofiles
from pathlib import Path
from functools import lru_cache
import markdown
from concurrent.futures import ThreadPoolExecutor

class DocumentationCache:
    def __init__(self):
        self.content_cache = {}
        self.hash_cache = {}
        self.markdown_cache = {}
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

    def has_changed(self, key: str, content: str) -> bool:
        if key not in self.hash_cache:
            return True
        return self._hash_content(content) != self.hash_cache[key]

    @staticmethod
    def _hash_content(content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()

class DocumentationGenerator:
    def __init__(self):
        self.default_params = {
            "format": "markdown",
            "include_examples": True,
            "include_schemas": True
        }
        self.cache = DocumentationCache()
        self.pending_writes = {}

    async def generate_api_docs(self, endpoints: List[Dict], output_path: str = "docs/api.md") -> str:
        """Generate API documentation from endpoint definitions with caching"""
        doc_content = "# API Documentation\n\n"
        
        for endpoint in endpoints:
            doc_content += f"## {endpoint['method']} {endpoint['path']}\n\n"
            if 'description' in endpoint:
                doc_content += f"{endpoint['description']}\n\n"
            
            if 'request_schema' in endpoint:
                doc_content += "### Request Schema\n```json\n"
                doc_content += json.dumps(endpoint['request_schema'], indent=2)
                doc_content += "\n```\n\n"
            
            if 'response_schema' in endpoint:
                doc_content += "### Response Schema\n```json\n"
                doc_content += json.dumps(endpoint['response_schema'], indent=2)
                doc_content += "\n```\n\n"
            
            if 'example' in endpoint:
                doc_content += "### Example\n```bash\n"
                doc_content += endpoint['example']
                doc_content += "\n```\n\n"

        # Only write if content has changed
        if self.cache.has_changed('api_docs', doc_content):
            self.cache.set_content('api_docs', doc_content)
            self.pending_writes[output_path] = doc_content
            await self._batch_write()
        
        return doc_content

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

    async def process_markdown(self, content: str, cache_key: str) -> str:
        """Process markdown content asynchronously with caching"""
        if not self.cache.has_changed(cache_key, content):
            cached_result = self.cache.get_markdown(cache_key)
            if cached_result:
                return cached_result

        # Process markdown in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.cache._executor,
            lambda: markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
        )
        
        self.cache.set_markdown(cache_key, result)
        return result

    async def generate_component_docs(self, components: List[Dict], output_path: str = "docs/components.md") -> str:
        """Generate documentation for UI components with caching"""
        doc_content = "# Component Documentation\n\n"
        
        for component in components:
            doc_content += f"## {component['name']}\n\n"
            if 'description' in component:
                doc_content += f"{component['description']}\n\n"
            
            if 'props' in component:
                doc_content += "### Props\n\n"
                for prop, details in component['props'].items():
                    doc_content += f"- `{prop}`: {details['type']}"
                    if 'required' in details and details['required']:
                        doc_content += " (Required)"
                    if 'description' in details:
                        doc_content += f"\n  - {details['description']}"
                    doc_content += "\n"
                doc_content += "\n"
            
            if 'example' in component:
                doc_content += "### Example\n```html\n"
                doc_content += component['example']
                doc_content += "\n```\n\n"
        
        if self.cache.has_changed('component_docs', doc_content):
            self.cache.set_content('component_docs', doc_content)
            self.pending_writes[output_path] = doc_content
            await self._batch_write()
        
        return doc_content

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
                        with open(path, 'w') as f:
                            if content:
                                f.write(content)
                except Exception as e:
                    print(f"Error creating {path}: {str(e)}")
        
        create_structure(template, base)

    def validate_template(self, template: Dict) -> bool:
        """Validate directory structure template"""
        def validate_node(node):
            if isinstance(node, dict):
                return all(validate_node(value) for value in node.values())
            return isinstance(node, (str, type(None)))
        
        return validate_node(template)
