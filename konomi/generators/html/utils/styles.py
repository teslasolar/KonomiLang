"""
Style management utilities for HTML components
"""
from typing import Dict, Optional, Union

class StyleHelper:
    """Helper class for managing component styles."""
    
    @staticmethod
    def merge_styles(*style_dicts: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Merge multiple style dictionaries, later ones take precedence."""
        result = {}
        for style_dict in style_dicts:
            if style_dict:
                result.update(style_dict)
        return result
    
    @staticmethod
    def format_style(styles: Optional[Dict[str, str]]) -> str:
        """Format style dictionary into CSS string."""
        if not styles:
            return ""
        return "; ".join(f"{k}: {v}" for k, v in styles.items())
    
    @staticmethod
    def parse_style(style_str: str) -> Dict[str, str]:
        """Parse CSS style string into dictionary."""
        if not style_str:
            return {}
        return dict(
            pair.split(": ", 1) 
            for pair in style_str.split("; ") 
            if ": " in pair
        )
