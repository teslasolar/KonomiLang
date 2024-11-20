"""
SVG Generator module for Konomi Language
Provides utilities for programmatic SVG generation with animation support
"""
from typing import Dict, List, Optional, Union
import html
import re

class SVGGenerator:
    # SVG namespace and animation constants
    SVG_NAMESPACE = "http://www.w3.org/2000/svg"
    XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
    
    # Valid animation triggers
    VALID_TRIGGERS = {'click', 'mouseover', 'mouseout', 'mouseenter', 'mouseleave', 'focus', 'blur'}
    
    # Valid transform types
    VALID_TRANSFORM_TYPES = {'translate', 'scale', 'rotate', 'skewX', 'skewY'}
    
    # Valid timing functions with corresponding keySplines values
    VALID_TIMING_FUNCTIONS = {
        'linear': '0 0 1 1',
        'ease': '0.25 0.1 0.25 1',
        'ease-in': '0.42 0 1 1',
        'ease-out': '0 0 0.58 1',
        'ease-in-out': '0.42 0 0.58 1'
    }
    
    def __init__(self, width: int = 800, height: int = 600):
        """Initialize SVG generator with dimensions."""
        self.width = width
        self.height = height
        self.elements: List[str] = []
        self.defs: List[str] = []
        self.animations: List[str] = []
        self.scripts: List[str] = []
        self.has_interactive = False
        
    def _format_style(self, style: Optional[Dict[str, str]]) -> str:
        """Format style dictionary to CSS string."""
        if not style:
            return ""
        return ";".join(f"{k}:{v}" for k, v in style.items())
    
    def _validate_attribute_name(self, name: str) -> bool:
        """Validate SVG attribute name."""
        return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9\-_]*$', name))
        
    def _escape_attribute_value(self, value: str) -> str:
        """Escape attribute value."""
        return html.escape(value, quote=True)
"""
SVG Generator module for Konomi Language
Provides utilities for programmatic SVG generation with animation support
"""
from typing import Dict, List, Optional, Union
import html
import re
from xml.sax.saxutils import escape, quoteattr

class SVGGenerator:
    # SVG namespace attributes
    SVG_NAMESPACE = "http://www.w3.org/2000/svg"
    XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
    
    # Valid SVG attribute pattern
    VALID_ATTR_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-_:]*$')
    
    # Valid style properties
    VALID_STYLE_PROPERTIES = {
        'fill', 'stroke', 'stroke-width', 'opacity', 'font-size', 
        'font-family', 'text-anchor', 'transform', 'style', 'cursor'
    }
    # Valid SVG transform types
    VALID_TRANSFORM_TYPES = {
        'translate', 'scale', 'rotate', 'skewX', 'skewY', 'matrix'
    }

    # Valid animation timing functions with corresponding keySplines values
    VALID_TIMING_FUNCTIONS = {
        'linear': '0 0 1 1',
        'ease': '0.25 0.1 0.25 1',
        'ease-in': '0.42 0 1 1',
        'ease-out': '0 0 0.58 1',
        'ease-in-out': '0.42 0 0.58 1',
        'step-start': '0 0 1 1',
        'step-end': '0 0 1 1'
    }

    # Valid animation triggers
    VALID_TRIGGERS = {
        'click', 'mouseover', 'mouseout', 'focusin', 'focusout'
    }

    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.elements: List[str] = []
        self.defs: List[str] = []
        self.animations: List[str] = []

    def _validate_attribute_name(self, name: str) -> bool:
        """Validate XML attribute name."""
        return bool(self.VALID_ATTR_PATTERN.match(name))

    def _validate_style_property(self, prop: str) -> bool:
        """Validate CSS style property name."""
        return prop in self.VALID_STYLE_PROPERTIES

    def _escape_attribute_value(self, value: str) -> str:
        """Escape attribute value properly."""
        return quoteattr(str(value))[1:-1]  # Remove surrounding quotes

    def _format_style(self, style: Dict[str, str]) -> str:
        """Format style dictionary into SVG style string with validation."""
        if not style:
            return ""
        
        valid_styles = []
        for k, v in style.items():
            if self._validate_style_property(k):
                escaped_value = self._escape_attribute_value(v)
                valid_styles.append(f"{k}:{escaped_value}")
            else:
                raise ValueError(f"Invalid style property: {k}")
        
        return ';'.join(valid_styles)

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
    def add_path(self, d: str, style: Optional[Dict[str, str]] = None, id: Optional[str] = None) -> None:
        """Add a path to the SVG.
        
        Args:
            d: Path data string
            style: Optional style dictionary
            id: Optional element ID
        """
        style_str = f' style="{self._format_style(style)}"' if style else ''
        id_str = f' id="{id}"' if id else ''
        self.elements.append(
            f'<path d="{d}"{style_str}{id_str}/>'
        )


    def add_animation(self, target_id: str, attribute: str, duration: int,
                     keyframes: Dict[str, Dict[str, str]], 
                     repeat_count: Union[int, str] = "indefinite") -> None:
        """Add an animation to an SVG element."""
        if not self._validate_attribute_name(attribute):
            raise ValueError(f"Invalid attribute name: {attribute}")
        
        # Validate and escape values
        values = self._format_keyframes(keyframes)
        escaped_values = self._escape_attribute_value(values)
        escaped_repeat = self._escape_attribute_value(str(repeat_count))
        
        # Create animation element with proper XML structure
        self.animations.append(
            f'<animate xlink:href="#{target_id}" '
            f'attributeName="{attribute}" '
            f'dur="{duration}s" '
            f'values="{escaped_values}" '
            f'repeatCount="{escaped_repeat}" '
            f'calcMode="spline" '
            f'keyTimes="0;1" '
            f'keySplines="0.4 0 0.2 1"/>'
        )
    def add_interactive_animation(self, target_id: str, trigger: str,
                               transform_type: str, from_val: str, to_val: str,
                               duration: float, timing: str = 'ease',
                               repeat_count: Optional[Union[int, str]] = "1") -> None:
        """Add an interactive animation triggered by user events.
        
        Args:
            target_id: ID of the target element
            trigger: Event trigger ('click', 'mouseover', etc.)
            transform_type: Type of transform animation
            from_val: Starting value
            to_val: Ending value
            duration: Animation duration in seconds
            timing: Timing function name
            repeat_count: Number of times to repeat or "indefinite"
        """
        if not target_id:
            raise ValueError("target_id is required")
        if trigger not in self.VALID_TRIGGERS:
            raise ValueError(f"Invalid trigger: {trigger}")
        if timing not in self.VALID_TIMING_FUNCTIONS:
            raise ValueError(f"Invalid timing function: {timing}")
        if transform_type not in self.VALID_TRANSFORM_TYPES:
            raise ValueError(f"Invalid transform type: {transform_type}")

        animation_id = f"{target_id}-{trigger}-animation"
        self.has_interactive = True
        
        # Add animation element with proper SMIL attributes
        self.defs.append(
            f'<animateTransform id="{animation_id}" '
            f'xlink:href="#{target_id}" '
            f'attributeName="transform" '
            f'type="{transform_type}" '
            f'from="{from_val}" '
            f'to="{to_val}" '
            f'dur="{duration}s" '
            f'begin="{target_id}.{trigger}" '
            f'calcMode="spline" '
            f'keySplines="{self.VALID_TIMING_FUNCTIONS[timing]}" '
            f'additive="replace" '
            f'fill="freeze" '
            f'restart="whenNotActive" '
            f'repeatCount="{repeat_count}"/>'
        )

    def _get_timing_spline(self, timing: str) -> str:
        """Get the keySplines value for a timing function."""
        splines = {
            'linear': '0 0 1 1',
            'ease': '0.25 0.1 0.25 1',
            'ease-in': '0.42 0 1 1',
            'ease-out': '0 0 0.58 1',
            'ease-in-out': '0.42 0 0.58 1'
        }
        return splines.get(timing, '0.25 0.1 0.25 1')  # Default to 'ease'

    def add_morph_animation(self, target_id: str, path1: str, path2: str,
                          duration: int, trigger: str = None,
                          timing: str = 'ease') -> None:
        """Add a path morphing animation.
        
        Args:
            target_id: ID of the target path element
            path1: Initial path data
            path2: Final path data
            duration: Animation duration in seconds
            trigger: Optional event trigger
            timing: Timing function name
        """
        if trigger and trigger not in self.VALID_TRIGGERS:
            raise ValueError(f"Invalid trigger: {trigger}")
        if timing not in self.VALID_TIMING_FUNCTIONS:
            raise ValueError(f"Invalid timing function: {timing}")

        begin = f"#{target_id}.{trigger}" if trigger else "0s"
        self.defs.append(
            f'<animate '
            f'xlink:href="#{target_id}" '
            f'attributeName="d" '
            f'from="{path1}" to="{path2}" '
            f'dur="{duration}s" '
            f'begin="{begin}" '
            f'calcMode="spline" '
            f'keySplines="{self._get_timing_spline(timing)}" '
            f'fill="freeze"/>'
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
        """Generate the complete SVG document with animations."""
        defs_str = '\n    '.join(self.defs)
        elements_str = '\n    '.join(self.elements)
        
        # Add script for handling animation triggers
        script = """
    <script type="text/javascript"><![CDATA[
        function initInteractiveAnimations() {
            const svg = document.querySelector('svg');
            if (!svg) return;
            
            function getAnimationsForElement(elementId) {
                return [
                    ...svg.querySelectorAll(`animate[xlink\\:href="#${elementId}"]`),
                    ...svg.querySelectorAll(`animateTransform[xlink\\:href="#${elementId}"]`)
                ];
            }
            
            function setupEventHandler(element, trigger, animation) {
                element.style.cursor = 'pointer';
                element.addEventListener(trigger, () => {
                    // Reset animation if it's already running
                    animation.endElement();
                    // Start the animation
                    animation.beginElement();
                });
            }
            
            function initElement(element) {
                if (!element.id) return;
                
                const animations = getAnimationsForElement(element.id);
                animations.forEach(animation => {
                    const begin = animation.getAttribute('begin');
                    if (!begin || !begin.includes(element.id)) return;
                    
                    const trigger = begin.split('.')[1];
                    if (!trigger) return;
                    
                    setupEventHandler(element, trigger, animation);
                });
            }
            
            // Initialize all elements with IDs
            const elements = svg.getElementsByTagName('*');
            Array.from(elements).forEach(initElement);
        }
        
        // Initialize animations when the document is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initInteractiveAnimations);
        } else {
            initInteractiveAnimations();
        }
    ]]></script>"""
        
        defs_section = f"<defs>\n    {defs_str}\n</defs>\n    " if self.defs else ""
        
        return f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n    {defs_section}{elements_str}\n    {script}\n</svg>'