"""
Documentation Generator for KonomiLang
Handles automatic generation of documentation, API endpoints, and directory structure
"""
from typing import Dict, List, Optional
import os
import json
from pathlib import Path

class DocumentationGenerator:
    def __init__(self):
        self.default_params = {
            "format": "markdown",
            "include_examples": True,
            "include_schemas": True
        }
    
    def generate_api_docs(self, endpoints: List[Dict], output_path: str = "docs/api.md") -> str:
        """Generate API documentation from endpoint definitions"""
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
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(doc_content)
        
        return doc_content
    
    def generate_directory_structure(self, template: Dict[str, any], base_path: str = ".") -> None:
        """Generate directory structure based on template"""
        base = Path(base_path)
        
        def create_structure(structure: Dict, current_path: Path):
            for name, content in structure.items():
                path = current_path / name
                
                if isinstance(content, dict):
                    # It's a directory
                    path.mkdir(exist_ok=True)
                    create_structure(content, path)
                else:
                    # It's a file
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, 'w') as f:
                        if content:
                            f.write(content)
        
        create_structure(template, base)
    
    def discover_endpoints(self, app) -> List[Dict]:
        """Discover all endpoints in a Flask application"""
        endpoints = []
        
        for rule in app.url_map.iter_rules():
            endpoint_data = {
                "path": rule.rule,
                "method": list(rule.methods - {"HEAD", "OPTIONS"})[0],
                "name": rule.endpoint,
                "description": app.view_functions[rule.endpoint].__doc__
            }
            
            # Add example request if available
            if hasattr(app.view_functions[rule.endpoint], 'example'):
                endpoint_data['example'] = app.view_functions[rule.endpoint].example
            
            endpoints.append(endpoint_data)
        
        return endpoints
    
    def generate_component_docs(self, components: List[Dict], output_path: str = "docs/components.md") -> str:
        """Generate documentation for UI components"""
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
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(doc_content)
        
        return doc_content

    def validate_template(self, template: Dict) -> bool:
        """Validate directory structure template"""
        def validate_node(node):
            if isinstance(node, dict):
                return all(validate_node(value) for value in node.values())
            return isinstance(node, (str, type(None)))
        
        return validate_node(template)
