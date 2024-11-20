"""
HTML Component Library with Custom Elements
Provides a collection of reusable HTML components with customizable properties
"""
from typing import Dict, List, Optional, Union
import html
from dataclasses import dataclass
from ..html_generator import HTMLGenerator

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
        
    def _format_attributes(self) -> str:
        """Format component attributes."""
        attrs = {}
        if self.props.class_name:
            attrs['class'] = self.props.class_name
        if self.props.id:
            attrs['id'] = self.props.id
        if self.props.attributes:
            attrs.update(self.props.attributes)
            
        return ' '.join(f'{k}="{html.escape(str(v))}"' for k, v in attrs.items())

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

@dataclass
class CardProps(ComponentProps):
    """Card component properties."""
    padding: str = "normal"  # compact, normal, large
    shadow: str = "medium"   # none, small, medium, large
    border: bool = True
    hover_effect: bool = False

class Card(Component):
    """Card component for content containers."""
    
    PADDING = {
        "compact": "p-2",
        "normal": "p-4",
        "large": "p-6"
    }
    
    SHADOWS = {
        "none": "",
        "small": "shadow-sm",
        "medium": "shadow",
        "large": "shadow-lg"
    }
    
    def __init__(self, content: str, props: Optional[CardProps] = None):
        super().__init__(props or CardProps())
        self.content = content
        self.props: CardProps = self.props  # Type hint for IDE
        
    def render(self) -> str:
        padding = self.PADDING.get(self.props.padding, self.PADDING["normal"])
        shadow = self.SHADOWS.get(self.props.shadow, self.SHADOWS["medium"])
        
        classes = [
            "bg-white rounded-lg",
            padding,
            shadow
        ]
        
        if self.props.border:
            classes.append("border border-gray-200")
        if self.props.hover_effect:
            classes.append("transition-shadow duration-200 hover:shadow-lg")
        if self.props.class_name:
            classes.append(self.props.class_name)
            
        attrs = {'class': ' '.join(classes)}
        if self.props.id:
            attrs['id'] = self.props.id
            
        return self.generator.generate_element(
            'div',
            content=self.content,
            attributes=attrs
        )

@dataclass
class AlertProps(ComponentProps):
    """Alert component properties."""
    type: str = "info"  # info, success, warning, error
    dismissible: bool = False

class Alert(Component):
    """Alert component for notifications and messages."""
    
    TYPES = {
        "info": {
            "bg": "bg-blue-50",
            "text": "text-blue-700",
            "icon": "info-circle"
        },
        "success": {
            "bg": "bg-green-50",
            "text": "text-green-700",
            "icon": "check-circle"
        },
        "warning": {
            "bg": "bg-yellow-50",
            "text": "text-yellow-700",
            "icon": "exclamation-triangle"
        },
        "error": {
            "bg": "bg-red-50",
            "text": "text-red-700",
            "icon": "exclamation-circle"
        }
    }
    
    def __init__(self, message: str, props: Optional[AlertProps] = None):
        super().__init__(props or AlertProps())
        self.message = message
        self.props: AlertProps = self.props  # Type hint for IDE
        
    def render(self) -> str:
        style = self.TYPES.get(self.props.type, self.TYPES["info"])
        
        classes = [
            "rounded-md p-4",
            style["bg"],
            style["text"]
        ]
        
        if self.props.class_name:
            classes.append(self.props.class_name)
            
        attrs = {'class': ' '.join(classes)}
        if self.props.id:
            attrs['id'] = self.props.id
            
        content = f'<div class="flex">'
        # Add icon
        content += f'<div class="flex-shrink-0"><i class="fas fa-{style["icon"]}"></i></div>'
        # Add message
        content += f'<div class="ml-3"><p class="text-sm">{html.escape(self.message)}</p></div>'
        
        if self.props.dismissible:
            content += '''
                <div class="ml-auto pl-3">
                    <button type="button" class="inline-flex rounded-md p-1.5 hover:bg-opacity-20 hover:bg-black focus:outline-none"
                            onclick="this.closest('.alert').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            '''
        
        content += '</div>'
            
        return self.generator.generate_element(
            'div',
            content=content,
            attributes=attrs
        )
