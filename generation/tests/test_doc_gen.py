import unittest
from ..functions.doc_gen import DocumentationGenerator
import tempfile
import os
import json
from pathlib import Path

class TestDocumentationGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DocumentationGenerator()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_api_docs_generation(self):
        endpoints = [{
            "method": "GET",
            "path": "/api/test",
            "description": "Test endpoint",
            "request_schema": {"type": "object"},
            "response_schema": {"type": "object"},
            "example": "curl http://localhost:5000/api/test"
        }]
        
        output_path = os.path.join(self.temp_dir, "api.md")
        content = self.generator.generate_api_docs(endpoints, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn("# API Documentation", content)
        self.assertIn("## GET /api/test", content)
    
    def test_directory_structure_generation(self):
        template = {
            "src": {
                "main.py": "print('Hello')",
                "utils": {
                    "__init__.py": "",
                    "helpers.py": "# Helper functions"
                }
            }
        }
        
        self.generator.generate_directory_structure(template, self.temp_dir)
        
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "src")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "src", "main.py")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "src", "utils", "helpers.py")))
    
    def test_component_docs_generation(self):
        components = [{
            "name": "Button",
            "description": "A reusable button component",
            "props": {
                "text": {
                    "type": "string",
                    "required": True,
                    "description": "Button text"
                }
            },
            "example": "<Button text=\"Click me\" />"
        }]
        
        output_path = os.path.join(self.temp_dir, "components.md")
        content = self.generator.generate_component_docs(components, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn("# Component Documentation", content)
        self.assertIn("## Button", content)
    
    def test_template_validation(self):
        valid_template = {
            "src": {
                "main.py": "content",
                "utils": {
                    "__init__.py": None
                }
            }
        }
        
        invalid_template = {
            "src": {
                "main.py": 123  # Invalid content type
            }
        }
        
        self.assertTrue(self.generator.validate_template(valid_template))
        self.assertFalse(self.generator.validate_template(invalid_template))
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
