"""
Common utilities for HTML components
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass
import html
from ...html_generator import HTMLGenerator
from ..decorators import api_doc, depends_on
from ..utils.validation import ValidationHelper
from ..utils.styles import StyleHelper

@dataclass
class ComponentProps:
    """Base class for component properties."""
    class_name: Optional[str] = None
    id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None

class Component:
    """Base component class with common functionality."""
    
    def __init__(self, props: Optional[ComponentProps] = None):
        self.props = props or ComponentProps()
        self.generator = HTMLGenerator()
        self.validator = ValidationHelper()
        self.style_helper = StyleHelper()
        self._validate_props()
    
    def _validate_props(self) -> None:
        """Validate component properties."""
        self.validator.validate_class_name(self.props.class_name)
        self.validator.validate_identifier(self.props.id, "id")
        self.validator.validate_attributes(self.props.attributes)
    
    @api_doc(
        description="Format component attributes into HTML string",
        inputs={
            "extra_attrs": "Additional attributes to include",
            "extra_classes": "Additional CSS classes to add"
        },
        outputs="Formatted HTML attribute string",
        example='''
        attrs = component._format_attributes(
            extra_attrs={"data-test": "value"},
            extra_classes="mt-4 p-2"
        )
        '''
    )
    def _format_attributes(self, 
                         extra_attrs: Optional[Dict[str, Any]] = None,
                         extra_classes: Optional[str] = None) -> str:
        """Format component attributes with optional extras."""
        attrs = {}
        
        # Handle classes
        classes = []
        if self.props.class_name:
            classes.append(self.props.class_name)
        if extra_classes:
            classes.append(extra_classes)
        if classes:
            attrs['class'] = ' '.join(classes)
            
        # Handle other attributes
        if self.props.id:
            attrs['id'] = self.props.id
        if self.props.attributes:
            attrs.update(self.props.attributes)
        if extra_attrs:
            attrs.update(extra_attrs)
            
        return ' '.join(f'{k}="{html.escape(str(v))}"' for k, v in attrs.items())
