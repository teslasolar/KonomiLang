"""
Tests for Generated Components
"""
import unittest
from unittest.mock import Mock, patch
import tempfile
import shutil
import os
from pathlib import Path
import json
from generation.functions.doc_gen import DocumentationGenerator
from konomi.utils.directory_manager import DirectoryManager

class TestGeneratedComponents(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.doc_gen = DocumentationGenerator(template_dir=self.temp_dir)
        self.dir_manager = DirectoryManager(self.temp_dir)
        
        # Create test templates
        os.makedirs(os.path.join(self.temp_dir, "templates"))
        with open(os.path.join(self.temp_dir, "templates/test.md.j2"), "w") as f:
            f.write("# {{ title }}\n\n{{ content }}")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    async def test_api_docs_generation(self):
        """Test API documentation generation"""
        test_endpoints = [
            {
                'path': '/api/test',
                'methods': ['GET'],
                'description': 'Test endpoint',
                'parameters': {
                    'id': {'type': 'integer', 'required': True}
                },
                'response_schema': {
                    'type': 'object',
                    'properties': {'message': {'type': 'string'}}
                }
            }
        ]
        
        output_path = os.path.join(self.temp_dir, "api_docs.md")
        content = await self.doc_gen.generate_api_docs(test_endpoints, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn('Test endpoint', content)
        self.assertIn('/api/test', content)

    async def test_error_docs_generation(self):
        """Test error documentation generation"""
        test_errors = [
            {
                'code': 'ERR001',
                'message': 'Test error',
                'description': 'This is a test error'
            }
        ]
        
        output_path = os.path.join(self.temp_dir, "error_docs.md")
        content = await self.doc_gen.generate_error_docs(test_errors, output_path)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertIn('ERR001', content)
        self.assertIn('Test error', content)

    def test_directory_structure_generation(self):
        """Test directory structure generation"""
        test_template = {
            'src': {
                'main.py': 'print("Hello")',
                'utils': {
                    '__init__.py': None
                }
            }
        }
        
        self.doc_gen.generate_directory_structure(test_template, self.temp_dir)
        
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src/main.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'src/utils/__init__.py')))
        
        with open(os.path.join(self.temp_dir, 'src/main.py')) as f:
            content = f.read()
            self.assertEqual(content, 'print("Hello")')

    @patch('generation.functions.doc_gen.Environment')
    async def test_template_rendering(self, mock_env):
        """Test template rendering with caching"""
        mock_template = Mock()
        mock_template.render_async.return_value = "# Test\n\nTest content"
        mock_env.return_value.get_template.return_value = mock_template
        
        content = await self.doc_gen.render_template(
            "test.md.j2",
            {"title": "Test", "content": "Test content"},
            cache_key="test"
        )
        
        self.assertIn("Test", content)
        self.assertIn("Test content", content)
        
        # Test caching
        cached_content = await self.doc_gen.render_template(
            "test.md.j2",
            {"title": "Test", "content": "Test content"},
            cache_key="test"
        )
        self.assertEqual(content, cached_content)

    def test_template_validation(self):
        """Test template validation logic"""
        valid_template = {
            'src': {
                'main.py': 'print("Hello")',
                'utils': None
            }
        }
        self.assertTrue(self.doc_gen.validate_template(valid_template))
        
        invalid_template = {
            'src': {
                'main.py': 123,  # Invalid: not string or dict
                'utils': None
            }
        }
        self.assertFalse(self.doc_gen.validate_template(invalid_template))

    def test_markdown_processing(self):
        """Test markdown processing with caching"""
        test_markdown = "# Test\n\n```python\nprint('hello')\n```"
        
        async def test_markdown_processing():
            processed = await self.doc_gen.process_markdown(test_markdown, "test_md")
            self.assertIn("<h1>", processed)
            self.assertIn("<code>", processed)
            
            # Test caching
            cached = await self.doc_gen.process_markdown(test_markdown, "test_md")
            self.assertEqual(processed, cached)
        
        import asyncio
        asyncio.run(test_markdown_processing())

    def test_directory_manager_integration(self):
        """Test directory manager integration with generated components"""
        test_structure = {
            'docs': {
                'api.md': '# API Documentation',
                'examples': {
                    'basic.md': '# Basic Examples'
                }
            }
        }
        
        # Test structure creation
        self.assertTrue(self.dir_manager.create_structure(test_structure))
        
        # Test structure export
        export_path = os.path.join(self.temp_dir, 'structure.json')
        self.assertTrue(self.dir_manager.export_template(export_path))
        
        # Test structure import
        imported = self.dir_manager.import_template(export_path)
        self.assertEqual(imported['docs']['api.md'], '# API Documentation')

if __name__ == '__main__':
    unittest.main()
