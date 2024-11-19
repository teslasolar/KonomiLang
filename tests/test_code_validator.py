"""
Tests for the Code Validation System
"""
import unittest
from konomi.utils.code_validator import CodeValidator

class TestCodeValidator(unittest.TestCase):
    def setUp(self):
        self.validator = CodeValidator()

    def test_syntax_validation(self):
        # Valid code
        valid_code = """
def hello_world():
    print("Hello, World!")
"""
        is_valid, errors = self.validator.validate_syntax(valid_code)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

        # Invalid code
        invalid_code = """
def hello_world()
    print("Hello, World!")
"""
        is_valid, errors = self.validator.validate_syntax(invalid_code)
        self.assertFalse(is_valid)
        self.assertTrue(len(errors) > 0)

    def test_style_validation(self):
        # Valid style
        valid_code = """
class MyClass:
    def my_function(self):
        return "Hello"
"""
        is_valid, violations = self.validator.validate_style(valid_code)
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)

        # Invalid style
        invalid_code = """
class myClass:
    def MyFunction(self):
        return "This is a very long line that exceeds the maximum line length limit of 100 characters which is not good practice"
"""
        is_valid, violations = self.validator.validate_style(invalid_code)
        self.assertFalse(is_valid)
        self.assertTrue(len(violations) > 0)

    def test_security_validation(self):
        # Secure code
        secure_code = """
def process_data(data):
    return data.upper()
"""
        is_valid, issues = self.validator.validate_security(secure_code)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)

        # Insecure code
        insecure_code = """
def process_data(data):
    api_key = "1234567890abcdef"
    password = "secret123"
    eval(data)
"""
        is_valid, issues = self.validator.validate_security(insecure_code)
        self.assertFalse(is_valid)
        self.assertTrue(len(issues) > 0)

    def test_comprehensive_validation(self):
        code = """
def process_data(data):
    api_key = "1234567890abcdef"
    return eval(data)
"""
        results = self.validator.validate_code(code)
        self.assertFalse(results['valid'])
        self.assertTrue(len(results['errors']) > 0)
        self.assertIn('security', results['details'])

    def test_validation_history(self):
        # Generate some validation issues
        self.validator.validate_code("""
def Bad_Function():
    password = "secret123"
    return eval("1 + 2")
""")

        # Check history
        summary = self.validator.get_validation_summary()
        self.assertTrue(len(summary['style_violations']) > 0)
        self.assertTrue(len(summary['security_issues']) > 0)

        # Clear history
        self.validator.clear_validation_history()
        summary = self.validator.get_validation_summary()
        self.assertEqual(len(summary['style_violations']), 0)
        self.assertEqual(len(summary['security_issues']), 0)

if __name__ == '__main__':
    unittest.main()
