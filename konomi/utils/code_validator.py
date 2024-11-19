"""
Code Validation System for KonomiLang
Handles validation of generated code against predefined rules and standards
"""
import ast
import re
from typing import Dict, List, Optional, Union, Tuple
import logging

logger = logging.getLogger(__name__)

class CodeValidator:
    def __init__(self):
        self.syntax_errors = []
        self.style_violations = []
        self.security_issues = []
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for validation operations"""
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler('validation_operations.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def validate_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate Python code syntax
        
        Args:
            code: String containing Python code
            
        Returns:
            Tuple of (is_valid, list of errors)
        """
        try:
            ast.parse(code)
            return True, []
        except SyntaxError as e:
            error = f"Syntax error at line {e.lineno}: {str(e)}"
            self.syntax_errors.append(error)
            return False, [error]
        except Exception as e:
            error = f"Validation error: {str(e)}"
            self.syntax_errors.append(error)
            return False, [error]

    def validate_style(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate code style against project standards
        
        Args:
            code: String containing Python code
            
        Returns:
            Tuple of (is_valid, list of violations)
        """
        violations = []
        
        # Check line length
        for i, line in enumerate(code.split('\n'), 1):
            if len(line) > 100:
                violations.append(f"Line {i} exceeds 100 characters")

        # Check naming conventions
        class_pattern = re.compile(r'class\s+(?!([A-Z][a-zA-Z0-9]*)|_)')
        function_pattern = re.compile(r'def\s+(?!([a-z_][a-z0-9_]*)|__)')
        
        for i, line in enumerate(code.split('\n'), 1):
            if class_pattern.search(line):
                violations.append(f"Invalid class name at line {i}")
            if function_pattern.search(line):
                violations.append(f"Invalid function name at line {i}")

        self.style_violations.extend(violations)
        return len(violations) == 0, violations

    def validate_security(self, code: str) -> Tuple[bool, List[str]]:
        """
        Check for common security issues
        
        Args:
            code: String containing Python code
            
        Returns:
            Tuple of (is_secure, list of security issues)
        """
        issues = []
        
        # Check for dangerous imports
        dangerous_imports = ['os.system', 'subprocess.call', 'eval', 'exec']
        for i, line in enumerate(code.split('\n'), 1):
            for dangerous_import in dangerous_imports:
                if dangerous_import in line:
                    issues.append(f"Potentially dangerous operation at line {i}: {dangerous_import}")

        # Check for hardcoded credentials
        credential_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret")
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern, issue_type in credential_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(f"{issue_type} found at line {i}")

        self.security_issues.extend(issues)
        return len(issues) == 0, issues

    def validate_code(self, code: str, validation_types: Optional[List[str]] = None) -> Dict:
        """
        Perform comprehensive code validation
        
        Args:
            code: String containing Python code
            validation_types: List of validation types to perform 
                            (defaults to ['syntax', 'style', 'security'])
        
        Returns:
            Dictionary containing validation results
        """
        if validation_types is None:
            validation_types = ['syntax', 'style', 'security']

        results = {
            'valid': True,
            'errors': [],
            'details': {}
        }

        try:
            if 'syntax' in validation_types:
                syntax_valid, syntax_errors = self.validate_syntax(code)
                results['details']['syntax'] = {
                    'valid': syntax_valid,
                    'errors': syntax_errors
                }
                results['valid'] &= syntax_valid
                results['errors'].extend(syntax_errors)

            if 'style' in validation_types:
                style_valid, style_violations = self.validate_style(code)
                results['details']['style'] = {
                    'valid': style_valid,
                    'violations': style_violations
                }
                results['valid'] &= style_valid
                results['errors'].extend(style_violations)

            if 'security' in validation_types:
                security_valid, security_issues = self.validate_security(code)
                results['details']['security'] = {
                    'valid': security_valid,
                    'issues': security_issues
                }
                results['valid'] &= security_valid
                results['errors'].extend(security_issues)

            logger.info(f"Validation completed: {'successful' if results['valid'] else 'failed'}")
            return results

        except Exception as e:
            error_msg = f"Validation failed: {str(e)}"
            logger.error(error_msg)
            return {
                'valid': False,
                'errors': [error_msg],
                'details': {}
            }

    def get_validation_summary(self) -> Dict:
        """Get summary of all validation issues"""
        return {
            'syntax_errors': self.syntax_errors,
            'style_violations': self.style_violations,
            'security_issues': self.security_issues
        }

    def clear_validation_history(self):
        """Clear all validation history"""
        self.syntax_errors.clear()
        self.style_violations.clear()
        self.security_issues.clear()
        logger.info("Validation history cleared")
