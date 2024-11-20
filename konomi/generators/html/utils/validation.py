"""
Shared validation utilities for HTML components
"""
import re
from typing import Dict, Any, Optional, Optional

class ValidationHelper:
    """Common validation functions for HTML components."""
    
    @staticmethod
    def validate_identifier(value: Optional[str], field_name: str) -> bool:
        """Validate HTML ID and other identifiers."""
        if not value:
            return True
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', value):
            raise ValueError(f"Invalid {field_name}: {value}. Must start with a letter and contain only letters, numbers, underscores, or hyphens.")
        return True
    
    @staticmethod
    def validate_class_name(value: Optional[str]) -> bool:
        """Validate CSS class names."""
        if not value:
            return True
        for class_name in value.split():
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', class_name):
                raise ValueError(f"Invalid class name: {class_name}")
        return True
    
    @staticmethod
    def validate_attributes(attributes: Optional[Dict[str, Any]]) -> bool:
        """Validate HTML attributes."""
        if not attributes:
            return True
        for key, value in attributes.items():
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', key):
                raise ValueError(f"Invalid attribute name: {key}")
            if not isinstance(value, (str, int, float, bool)):
                raise ValueError(f"Invalid attribute value type for {key}: {type(value)}")
        return True
