import unittest
from ..functions.doc_gen import DocumentationGenerator
import tempfile
import os
import json
from pathlib import Path
import asyncio

class TestDocumentationGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DocumentationGenerator()
        self.temp_dir = tempfile.mkdtemp()
        
    def asyncSetUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def asyncTearDown(self):
        self.loop.close()
    
    async def test_template_rendering(self):
        # Test API docs template
        endpoints = [{
            "method": "GET",
            "path": "/api/test",
            "description": "Test endpoint",
            "request_schema": {"type": "object"},
            "response_schema": {"type": "object"},
            "example": "curl http://localhost:5000/api/test"
        }]
        
        output_path = os.path.join(self.temp_dir, "api.md")
        content = await self.generator.generate_api_docs(endpoints, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn("# API Documentation", content)
        self.assertIn("## GET /api/test", content)
    
    async def test_syntax_docs_generation(self):
        syntax_data = {
            "sections": [
                {
                    "title": "Variables",
                    "description": "Variable declaration and usage",
                    "code_examples": [
                        {
                            "language": "konomi",
                            "code": "let x = 42",
                            "description": "Basic variable declaration"
                        }
                    ]
                }
            ],
            "best_practices": [
                "Use descriptive variable names",
                "Follow consistent formatting"
            ]
        }
        
        output_path = os.path.join(self.temp_dir, "syntax.md")
        content = await self.generator.generate_syntax_docs(syntax_data, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn("# Syntax Documentation", content)
        self.assertIn("## Variables", content)
        self.assertIn("let x = 42", content)
    
    async def test_component_docs_generation(self):
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
            "example": {
                "language": "html",
                "code": "<Button text=\"Click me\" />",
                "description": "Basic button usage"
            }
        }]
        
        output_path = os.path.join(self.temp_dir, "components.md")
        content = await self.generator.generate_component_docs(components, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn("# Component Documentation", content)
        self.assertIn("## Button", content)
        self.assertIn("Button text", content)
    
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
    
    def test_cache_functionality(self):
        key = "test_key"
        content = "test_content"
        
        # Test content cache
        self.generator.cache.set_content(key, content)
        self.assertEqual(self.generator.cache.get_content(key), content)
        
        # Test markdown cache
        markdown_content = "# Test"
        self.generator.cache.set_markdown(key, markdown_content)
        self.assertEqual(self.generator.cache.get_markdown(key), markdown_content)
        
        # Test change detection
        self.assertTrue(self.generator.cache.has_changed(key, "new_content"))
        self.assertFalse(self.generator.cache.has_changed(key, content))
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
