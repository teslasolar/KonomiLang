"""
HTML Form Components
Provides form-specific components with validation and styling
"""
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from .components import Component, ComponentProps, Input, InputProps, Button, ButtonProps

@dataclass
class FormProps(ComponentProps):
    """Form component properties."""
    method: str = "post"
    action: Optional[str] = None
    autocomplete: bool = True
    validate: bool = True

class Form(Component):
    """Form component with validation and submission handling."""
    
    def __init__(self, children: List[str], props: Optional[FormProps] = None):
        super().__init__(props or FormProps())
        self.children = children
        self.props: FormProps = self.props
        
    def render(self) -> str:
        attrs = {
            'method': self.props.method,
            'class': 'space-y-6'
        }
        
        if self.props.action:
            attrs['action'] = self.props.action
        if not self.props.autocomplete:
            attrs['autocomplete'] = 'off'
        if self.props.validate:
            attrs['novalidate'] = ''
        if self.props.class_name:
            attrs['class'] = f"{attrs['class']} {self.props.class_name}"
        if self.props.id:
            attrs['id'] = self.props.id
            
        return self.generator.generate_element(
            'form',
            content='\n'.join(self.children),
            attributes=attrs
        )

@dataclass
class FormGroupProps:
    """Form group component properties."""
    label: str  # Required argument first
    class_name: Optional[str] = None
    id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    help_text: Optional[str] = None
    required: bool = False
    error: Optional[str] = None

    def __post_init__(self):
        """Initialize parent class attributes after dataclass initialization."""
        self.class_name = self.class_name
        self.id = self.id
        self.attributes = self.attributes

class FormGroup(Component):
    """Form group component for input organization."""
    
    def __init__(self, input_component: str, props: Optional[FormGroupProps] = None):
        super().__init__(ComponentProps(
            class_name=props.class_name if props else None,
            id=props.id if props else None,
            attributes=props.attributes if props else None
        ))
        self.input_component = input_component
        self.props: FormGroupProps = props or FormGroupProps(label="")
        
    def render(self) -> str:
        label_classes = "block text-sm font-medium text-gray-700"
        if self.props.required:
            label_classes += " required"
            
        content = f'''
            <label class="{label_classes}">
                {self.props.label}
                {' <span class="text-red-500">*</span>' if self.props.required else ''}
            </label>
            <div class="mt-1">
                {self.input_component}
                {f'<p class="mt-1 text-sm text-gray-500">{self.props.help_text}</p>' if self.props.help_text else ''}
                {f'<p class="mt-1 text-sm text-red-600">{self.props.error}</p>' if self.props.error else ''}
            </div>
        '''
        
        classes = ["form-group"]
        if self.props.class_name:
            classes.append(self.props.class_name)
            
        attrs = {'class': ' '.join(classes)}
        if self.props.id:
            attrs['id'] = self.props.id
            
        return self.generator.generate_element(
            'div',
            content=content,
            attributes=attrs
        )

@dataclass
class SelectProps:
    """Select component properties."""
    options: List[Dict[str, str]]  # Required argument first
    class_name: Optional[str] = None
    id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    value: Optional[str] = None
    placeholder: Optional[str] = None
    required: bool = False
    disabled: bool = False
    multiple: bool = False

    def __post_init__(self):
        """Initialize parent class attributes after dataclass initialization."""
        self.class_name = self.class_name
        self.id = self.id
        self.attributes = self.attributes

class Select(Component):
    """Select component with options."""
    
    def __init__(self, props: Optional[SelectProps] = None):
        super().__init__(ComponentProps(
            class_name=props.class_name if props else None,
            id=props.id if props else None,
            attributes=props.attributes if props else None
        ))
        self.props: SelectProps = props or SelectProps(options=[])
        
    def render(self) -> str:
        base_classes = (
            "block w-full rounded-md border-gray-300 shadow-sm "
            "focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        )
        
        if self.props.class_name:
            base_classes = f"{base_classes} {self.props.class_name}"
            
        attrs = {'class': base_classes}
        
        if self.props.required:
            attrs['required'] = 'required'
        if self.props.disabled:
            attrs['disabled'] = 'disabled'
        if self.props.multiple:
            attrs['multiple'] = 'multiple'
        if self.props.id:
            attrs['id'] = self.props.id
            
        options_html = []
        if self.props.placeholder:
            options_html.append(
                f'<option value="" disabled selected>{self.props.placeholder}</option>'
            )
            
        for option in self.props.options:
            selected = 'selected' if option.get('value') == self.props.value else ''
            options_html.append(
                f'<option value="{option["value"]}" {selected}>{option["label"]}</option>'
            )
            
        return self.generator.generate_element(
            'select',
            content='\n'.join(options_html),
            attributes=attrs
        )
