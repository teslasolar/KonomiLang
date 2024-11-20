"""
Core SVG Generation functionality
"""
from typing import Dict, List, Optional, Union
import html
from .validation import SVGValidator
from .animations import AnimationManager

class SVGGenerator:
    """Base SVG Generator with core functionality."""
    
    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.elements: List[str] = []
        self.defs: List[str] = []
        self.validator = SVGValidator()
        self.animation_manager = AnimationManager()
        
    def add_element(self, element: str) -> None:
        """Add a raw SVG element."""
        self.elements.append(element)
        
    def add_definition(self, definition: str) -> None:
        """Add a definition element."""
        self.defs.append(definition)
        
    def generate(self) -> str:
        """Generate the complete SVG document."""
        defs_str = '\n    '.join(self.defs)
        elements_str = '\n    '.join(self.elements)
        
        defs_section = f"<defs>\n    {defs_str}\n</defs>\n    " if self.defs else ""
        
        return (
            f'<svg width="{self.width}" height="{self.height}" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink">\n'
            f'    {defs_section}{elements_str}\n'
            f'    {self.animation_manager.get_initialization_script()}\n'
            f'</svg>'
        )
