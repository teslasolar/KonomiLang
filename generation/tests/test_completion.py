import unittest
from ..functions.completion import CompletionGenerator

class TestCompletionGeneration(unittest.TestCase):
    def setUp(self):
        self.generator = CompletionGenerator()

    def test_prompt_validation(self):
        # Test empty prompt
        with self.assertRaises(ValueError):
            self.generator.validate_prompt("")
        
        # Test prompt length
        with self.assertRaises(ValueError):
            self.generator.validate_prompt("a" * 5000)  # Too long
            
        # Test valid prompt
        valid_prompt = "Generate a story about space exploration"
        self.assertTrue(self.generator.validate_prompt(valid_prompt))

    def test_generation_parameters(self):
        # Test invalid temperature
        with self.assertRaises(ValueError):
            self.generator.validate_params({"temperature": 2.5})
            
        # Test invalid max_tokens
        with self.assertRaises(ValueError):
            self.generator.validate_params({"max_tokens": -1})
            
        # Test valid parameters
        valid_params = {
            "temperature": 0.7,
            "max_tokens": 100,
            "top_p": 0.9
        }
        self.assertTrue(self.generator.validate_params(valid_params))

    def test_response_format(self):
        prompt = "Generate a short story"
        response = self.generator.generate(prompt)
        
        self.assertIsInstance(response, dict)
        self.assertIn("text", response)
        self.assertIn("usage", response)
        self.assertIn("model", response)

    def test_error_handling(self):
        # Test API error handling
        with self.assertRaises(Exception):
            self.generator.generate(None)
        
        # Test rate limit handling
        with self.assertRaises(Exception):
            for _ in range(100):  # Force rate limit
                self.generator.generate("Test prompt")
