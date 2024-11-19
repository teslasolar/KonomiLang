"""
Tests for the Dynamic Directory Structure Manager
"""
import unittest
import tempfile
import shutil
from pathlib import Path
import json
from konomi.utils.directory_manager import DirectoryManager

class TestDirectoryManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = DirectoryManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_validate_template(self):
        valid_template = {
            "src": {
                "main.py": "print('Hello')",
                "utils": {
                    "__init__.py": None
                }
            }
        }
        self.assertTrue(self.manager.validate_template(valid_template))

        invalid_template = {
            "src": {
                "main.py": 123  # Invalid content type
            }
        }
        self.assertFalse(self.manager.validate_template(invalid_template))

    def test_create_structure(self):
        template = {
            "src": {
                "main.py": "print('Hello')",
                "utils": {
                    "__init__.py": ""
                }
            }
        }
        self.assertTrue(self.manager.create_structure(template))
        
        # Verify structure was created
        src_path = Path(self.temp_dir) / "src"
        self.assertTrue(src_path.exists())
        self.assertTrue((src_path / "main.py").exists())
        self.assertTrue((src_path / "utils" / "__init__.py").exists())

    def test_list_directory(self):
        # Create some files and directories
        template = {
            "test_dir": {
                "file1.txt": "content",
                "subdir": {
                    "file2.txt": "content"
                }
            }
        }
        self.manager.create_structure(template)
        
        contents = self.manager.list_directory()
        self.assertEqual(len(contents), 1)  # Should have one root directory
        self.assertEqual(contents[0]['name'], "test_dir")
        self.assertEqual(contents[0]['type'], "directory")

    def test_remove_structure(self):
        # Create structure
        test_dir = Path(self.temp_dir) / "test_dir"
        test_dir.mkdir()
        (test_dir / "test_file.txt").write_text("content")
        
        # Test removal
        self.assertTrue(self.manager.remove_structure(test_dir))
        self.assertFalse(test_dir.exists())

    def test_get_structure(self):
        original_template = {
            "config": {
                "settings.json": '{"key": "value"}',
                "data": {
                    "info.txt": "content"
                }
            }
        }
        self.manager.create_structure(original_template)
        
        structure = self.manager.get_structure()
        self.assertIn("config", structure)
        self.assertIn("settings.json", structure["config"])
        self.assertIn("data", structure["config"])

    def test_export_import_template(self):
        original_template = {
            "src": {
                "main.py": "print('Test')",
                "utils": {
                    "__init__.py": None
                }
            }
        }
        
        # Export template
        export_path = Path(self.temp_dir) / "template.json"
        self.assertTrue(self.manager.export_template(export_path))
        
        # Import template
        imported_template = self.manager.import_template(export_path)
        self.assertIsNotNone(imported_template)
        
        # Create structure from imported template
        self.assertTrue(self.manager.create_structure(imported_template))

    def test_operation_history(self):
        template = {
            "test": {
                "file.txt": "content"
            }
        }
        
        # Perform operations
        self.manager.create_structure(template)
        self.manager.list_directory()
        
        # Check history
        history = self.manager.get_history()
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[0]['operation'], 'create_structure')
        
        # Clear history
        self.manager.clear_history()
        self.assertEqual(len(self.manager.get_history()), 0)

if __name__ == '__main__':
    unittest.main()
