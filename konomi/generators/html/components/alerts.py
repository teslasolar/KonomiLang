"""
Alert HTML components
"""
from typing import Optional
from dataclasses import dataclass
import html
from .utils import Component, ComponentProps

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
