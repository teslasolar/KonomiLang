"""
SVG Transform functionality
"""
from typing import Dict, List, Optional, Union
from .validation import SVGValidator

class TransformManager:
    """Manages SVG transform operations."""
    
    def __init__(self):
        self.validator = SVGValidator()
        
    def create_transform(
        self, transform_type: str,
        values: Union[str, Dict[str, str]],
        origin: Optional[str] = None
    ) -> str:
        """Create a transform attribute string.
        
        Args:
            transform_type: Type of transform (translate, scale, rotate, etc.)
            values: Transform values as string or dictionary
            origin: Optional transform origin
            
        Returns:
            Transform attribute string
        """
        self.validator.validate_transform_type(transform_type)
        
        if isinstance(values, dict):
            values_str = ' '.join(str(v) for v in values.values())
        else:
            values_str = str(values)
            
        transform = f"{transform_type}({values_str})"
        
        if origin:
            transform += f" transform-origin: {origin}"
            
        return transform
        
    def combine_transforms(self, transforms: List[str]) -> str:
        """Combine multiple transforms into a single attribute string."""
        return ' '.join(transforms)
