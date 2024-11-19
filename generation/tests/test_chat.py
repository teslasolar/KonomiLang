import unittest
from ..functions.chat import ChatGenerator

class TestChatGeneration(unittest.TestCase):
    def setUp(self):
        self.generator = ChatGenerator()

    def test_prompt_validation(self):
        # Test empty messages
        with self.assertRaises(ValueError):
            self.generator.validate_messages([])
        
        # Test invalid message format
        with self.assertRaises(ValueError):
            self.generator.validate_messages([{"invalid": "format"}])
            
        # Test valid messages
        valid_messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        self.assertTrue(self.generator.validate_messages(valid_messages))

    def test_generation_parameters(self):
        # Test invalid temperature
        with self.assertRaises(ValueError):
            self.generator.validate_params({"temperature": -1})
            
        # Test valid parameters
        valid_params = {
            "temperature": 0.8,
            "max_tokens": 150,
            "presence_penalty": 0.6
        }
        self.assertTrue(self.generator.validate_params(valid_params))

    def test_response_format(self):
        messages = [{"role": "user", "content": "What is AI?"}]
        response = self.generator.generate(messages)
        
        self.assertIsInstance(response, dict)
        self.assertIn("message", response)
        self.assertIn("usage", response)
        self.assertIn("model", response)

    def test_error_handling(self):
        # Test invalid role
        with self.assertRaises(ValueError):
            self.generator.generate([
                {"role": "invalid", "content": "test"}
            ])
        
        # Test context length
        with self.assertRaises(ValueError):
            self.generator.generate([
                {"role": "user", "content": "test"} for _ in range(100)
            ])
