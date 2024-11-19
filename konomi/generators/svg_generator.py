"""
SVG Generator module for Konomi Language
Provides utilities for programmatic SVG generation with animation support
"""
from typing import Dict, List, Optional, Union
import html

class SVGGenerator:
    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.elements: List[str] = []
        self.defs: List[str] = []
        self.animations: List[str] = []

    def _format_style(self, style: Dict[str, str]) -> str:
        """Format style dictionary into SVG style string."""
        return ';'.join(f"{k}:{v}" for k, v in style.items())

    def _format_keyframes(self, keyframes: Dict[str, Dict[str, str]]) -> str:
        """Format keyframes dictionary into SVG animation string."""
        return ';'.join(f"{time}% {{{';'.join(f'{k} {v}' for k, v in attrs.items())}}}"
                      for time, attrs in keyframes.items())

    def add_rect(self, x: float, y: float, width: float, height: float, 
                style: Dict[str, str] = None, id: str = None) -> None:
        """Add a rectangle to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        id_str = f' id="{id}"' if id else ''
        self.elements.append(
            f'<rect x="{x}" y="{y}" width="{width}" '
            f'height="{height}"{style_str}{id_str}/>'
        )

    def add_circle(self, cx: float, cy: float, r: float, 
                  style: Dict[str, str] = None, id: str = None) -> None:
        """Add a circle to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        id_str = f' id="{id}"' if id else ''
        self.elements.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}"{style_str}{id_str}/>'
        )

    def add_line(self, x1: float, y1: float, x2: float, y2: float, 
                style: Dict[str, str] = None, id: str = None) -> None:
        """Add a line to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        id_str = f' id="{id}"' if id else ''
        self.elements.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{style_str}{id_str}/>'
        )

    def add_text(self, x: float, y: float, text: str, 
                style: Dict[str, str] = None, id: str = None) -> None:
        """Add text to the SVG."""
        style_str = f' style="{self._format_style(style)}"' if style else ''
        id_str = f' id="{id}"' if id else ''
        self.elements.append(
            f'<text x="{x}" y="{y}"{style_str}{id_str}>{html.escape(text)}</text>'
        )

    def add_animation(self, target_id: str, attribute: str, duration: int,
                     keyframes: Dict[str, Dict[str, str]], 
                     repeat_count: Union[int, str] = "indefinite") -> None:
        """Add an animation to an SVG element."""
        values = self._format_keyframes(keyframes)
        self.animations.append(
            f'<animate attributeName="{attribute}" dur="{duration}s" '
            f'values="{values}" repeatCount="{repeat_count}" '
            f'calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/>'
        )

    def add_transform_animation(self, target_id: str, transform_type: str,
                              from_val: str, to_val: str, duration: int,
                              repeat_count: Union[int, str] = "indefinite") -> None:
        """Add a transform animation to an SVG element."""
        self.animations.append(
            f'<animateTransform attributeName="transform" type="{transform_type}" '
            f'from="{from_val}" to="{to_val}" dur="{duration}s" '
            f'repeatCount="{repeat_count}"/>'
        )

    def add_path_animation(self, target_id: str, path: str, duration: int,
                          repeat_count: Union[int, str] = "indefinite") -> None:
        """Add a motion path animation to an SVG element."""
        self.defs.append(f'<path id="motion-path" d="{path}" fill="none"/>')
        self.animations.append(
            f'<animateMotion dur="{duration}s" repeatCount="{repeat_count}">'
            f'<mpath href="#motion-path"/></animateMotion>'
        )

    def generate(self) -> str:
        """Generate the complete SVG document."""
        defs_str = '\n    '.join(self.defs)
        elements_with_animations = []
        
        for element in self.elements:
            if self.animations:
                # Insert animations before the closing tag
                element_parts = element.rsplit('/>', 1)
                if len(element_parts) == 2:
                    # Self-closing tag
                    elements_with_animations.append(
                        f"{element_parts[0]}\n        {chr(10).join(self.animations)}\n    />"
                    )
                else:
                    # Regular tag
                    element_parts = element.rsplit('</', 1)
                    elements_with_animations.append(
                        f"{element_parts[0]}\n        {chr(10).join(self.animations)}\n    </{element_parts[1]}"
                    )
            else:
                elements_with_animations.append(element)
        
        elements_str = '\n    '.join(elements_with_animations)
        defs_section = f"<defs>\n    {defs_str}\n</defs>\n    " if self.defs else ""
        
        return f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n    {defs_section}{elements_str}\n</svg>'
