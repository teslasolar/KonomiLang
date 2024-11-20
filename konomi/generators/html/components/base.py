"""
Base HTML components (Button, Input)
"""
from typing import Optional
from dataclasses import dataclass
import html
from .utils import Component, ComponentProps

@dataclass
class ButtonProps(ComponentProps):
    """Button component properties."""
    variant: str = "primary"  # primary, secondary, outline
    size: str = "medium"      # small, medium, large
    disabled: bool = False
    onclick: Optional[str] = None

class Button(Component):
    """Button component with various styles."""
    
    VARIANTS = {
        "primary": "bg-blue-600 hover:bg-blue-700 text-white",
        "secondary": "bg-gray-600 hover:bg-gray-700 text-white",
        "outline": "border-2 border-blue-600 hover:bg-blue-50 text-blue-600"
    }
    
    SIZES = {
        "small": "px-2 py-1 text-sm",
        "medium": "px-4 py-2",
        "large": "px-6 py-3 text-lg"
    }
    
    def __init__(self, text: str, props: Optional[ButtonProps] = None):
        super().__init__(props or ButtonProps())
        self.text = text
        self.props: ButtonProps = self.props  # Type hint for IDE
        
    def render(self) -> str:
        base_classes = "font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        variant_classes = self.VARIANTS.get(self.props.variant, self.VARIANTS["primary"])
        size_classes = self.SIZES.get(self.props.size, self.SIZES["medium"])
        
        classes = f"{base_classes} {variant_classes} {size_classes}"
        if self.props.class_name:
            classes = f"{classes} {self.props.class_name}"
            
        attrs = {
            'class': classes,
            'type': 'button'
        }
        
        if self.props.disabled:
            attrs['disabled'] = 'disabled'
        if self.props.onclick:
            attrs['onclick'] = self.props.onclick
        if self.props.id:
            attrs['id'] = self.props.id
            
        return self.generator.generate_element(
            'button',
            content=html.escape(self.text),
            attributes=attrs
        )

@dataclass
class InputProps(ComponentProps):
    """Input component properties."""
    type: str = "text"
    placeholder: Optional[str] = None
    value: Optional[str] = None
    required: bool = False
    disabled: bool = False
    pattern: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None

class Input(Component):
    """Input component with validation and styling."""
    
    def __init__(self, props: Optional[InputProps] = None):
        super().__init__(props or InputProps())
        self.props: InputProps = self.props  # Type hint for IDE
        
    def render(self) -> str:
        base_classes = (
            "block w-full rounded-md border-gray-300 shadow-sm "
            "focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        )
        
        if self.props.class_name:
            base_classes = f"{base_classes} {self.props.class_name}"
            
        attrs = {
            'class': base_classes,
            'type': self.props.type
        }
        
        if self.props.placeholder:
            attrs['placeholder'] = self.props.placeholder
        if self.props.value:
            attrs['value'] = self.props.value
        if self.props.required:
            attrs['required'] = 'required'
        if self.props.disabled:
            attrs['disabled'] = 'disabled'
        if self.props.pattern:
            attrs['pattern'] = self.props.pattern
        if self.props.min_length is not None:
            attrs['minlength'] = str(self.props.min_length)
        if self.props.max_length is not None:
            attrs['maxlength'] = str(self.props.max_length)
        if self.props.id:
            attrs['id'] = self.props.id
            
        return self.generator.generate_element(
            'input',
            attributes=attrs,
            self_closing=True
        )
