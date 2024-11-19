import unittest
from ..functions.code_gen import CodeGenerator

class TestCodeGeneration(unittest.TestCase):
    def setUp(self):
        self.generator = CodeGenerator()

    def test_prompt_validation(self):
        # Test empty prompt
        with self.assertRaises(ValueError):
            self.generator.validate_prompt("")
        
        # Test invalid language
        with self.assertRaises(ValueError):
            self.generator.validate_prompt("Generate code", language="invalid")
            
        # Test valid prompt
        valid_prompt = "Create a function to calculate fibonacci numbers"
        self.assertTrue(self.generator.validate_prompt(valid_prompt, language="python"))

    def test_generation_parameters(self):
        # Test invalid temperature
        with self.assertRaises(ValueError):
            self.generator.validate_params({"temperature": 3.0})
            
        # Test valid parameters
        valid_params = {
            "temperature": 0.3,
            "max_tokens": 500,
            "stop": ["```"]
        }
        self.assertTrue(self.generator.validate_params(valid_params))

    def test_response_format(self):
        prompt = "Write a hello world function in Python"
        response = self.generator.generate(prompt, language="python")
        
        self.assertIsInstance(response, dict)
        self.assertIn("code", response)
        self.assertIn("language", response)
        self.assertIn("usage", response)

    def test_error_handling(self):
        # Test syntax validation
        with self.assertRaises(ValueError):
            self.generator.validate_code("invalid python code")
        
        # Test unsupported language
        with self.assertRaises(ValueError):
            self.generator.generate("test", language="brainfuck")
