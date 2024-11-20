"""
Container HTML components (Card)
"""
from typing import Optional
from dataclasses import dataclass
from .utils import Component, ComponentProps

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
