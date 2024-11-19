"""
SVG Generator module for Konomi Language
Provides utilities for programmatic SVG generation
"""
from typing import Dict, List, Tuple, Union
import html

class SVGGenerator:
    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.elements: List[str] = []

    def _format_style(self, style: Dict[str, str]) -> str:
        """Format style dictionary into SVG style string."""
        return ';'.join(f"{k}:{v}" for k, v in style.items())

    def add_rect(self, x: float, y: float, width: float, height: float, 
                style: Dict[str, str] = None) -> None:
        """Add a rectangle to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        self.elements.append(
            f'<rect x="{x}" y="{y}" width="{width}" '
            f'height="{height}"{style_str}/>'
        )

    def add_circle(self, cx: float, cy: float, r: float, 
                  style: Dict[str, str] = None) -> None:
        """Add a circle to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        self.elements.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}"{style_str}/>'
        )

    def add_line(self, x1: float, y1: float, x2: float, y2: float, 
                style: Dict[str, str] = None) -> None:
        """Add a line to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        self.elements.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{style_str}/>'
        )

    def add_text(self, x: float, y: float, text: str, 
                style: Dict[str, str] = None) -> None:
        """Add text to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        self.elements.append(
            f'<text x="{x}" y="{y}"{style_str}>{html.escape(text)}</text>'
        )

    def generate(self) -> str:
        """Generate the complete SVG document."""
        elements_str = '\n    '.join(self.elements)
        return (f'<svg width="{self.width}" height="{self.height}" '
                f'xmlns="http://www.w3.org/2000/svg">\n    '
                f'{elements_str}\n</svg>')
