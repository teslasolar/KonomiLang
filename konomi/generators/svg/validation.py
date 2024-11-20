"""
SVG Validation functionality
"""
from typing import Dict, Set
import re

class SVGValidator:
    """Validates SVG elements and attributes."""
    
    # SVG Constants
    SVG_NAMESPACE = "http://www.w3.org/2000/svg"
    XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
    
    # Validation patterns
    VALID_ID_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-_]*$')
    VALID_ATTR_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-_:]*$')
    
    # Valid values
    VALID_TRANSFORM_TYPES: Set[str] = {
        'translate', 'scale', 'rotate', 'skewX', 'skewY', 'matrix'
    }
    
    VALID_TRIGGERS: Set[str] = {
        'click', 'mouseover', 'mouseout', 'focusin', 'focusout'
    }
    
    TIMING_FUNCTIONS: Dict[str, str] = {
        'linear': '0 0 1 1',
        'ease': '0.25 0.1 0.25 1',
        'ease-in': '0.42 0 1 1',
        'ease-out': '0 0 0.58 1',
        'ease-in-out': '0.42 0 0.58 1',
        'step-start': '0 0 1 1',
        'step-end': '0 0 1 1'
    }
    
    def validate_id(self, id_str: str) -> bool:
        """Validate an element ID."""
        if not id_str or not isinstance(id_str, str):
            raise ValueError("ID must be a non-empty string")
        if not self.VALID_ID_PATTERN.match(id_str):
            raise ValueError(f"Invalid ID format: {id_str}")
        return True
        
    def validate_transform_type(self, transform_type: str) -> bool:
        """Validate transform type."""
        if transform_type not in self.VALID_TRANSFORM_TYPES:
            raise ValueError(f"Invalid transform type: {transform_type}")
        return True
        
    def validate_trigger(self, trigger: str) -> bool:
        """Validate animation trigger."""
        if trigger not in self.VALID_TRIGGERS:
            raise ValueError(f"Invalid trigger: {trigger}")
        return True
        
    def validate_timing(self, timing: str) -> bool:
        """Validate timing function."""
        if timing not in self.TIMING_FUNCTIONS:
            raise ValueError(f"Invalid timing function: {timing}")
        return True
        
    def validate_transform_animation(
        self, target_id: str, trigger: str,
        transform_type: str, timing: str
    ) -> bool:
        """Validate transform animation parameters."""
        self.validate_id(target_id)
        self.validate_trigger(trigger)
        self.validate_transform_type(transform_type)
        self.validate_timing(timing)
        return True
        
    def get_timing_spline(self, timing: str) -> str:
        """Get keySplines value for timing function."""
        self.validate_timing(timing)
        return self.TIMING_FUNCTIONS[timing]
