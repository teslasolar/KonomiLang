"""
Navigation components
"""
from typing import List, Optional, Dict
from dataclasses import dataclass
from .utils import Component, ComponentProps

@dataclass
class NavItemProps(ComponentProps):
    """Navigation item properties."""
    class_name: Optional[str] = None
    id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    href: str = "#"
    active: bool = False
    icon: Optional[str] = None

class NavItem(Component):
    """Navigation item component."""
    
    def __init__(self, text: str, props: Optional[NavItemProps] = None):
        super().__init__(props or NavItemProps(href="#"))
        self.text = text
        self.props: NavItemProps = self.props
        
    def render(self) -> str:
        classes = [
            "px-3 py-2 rounded-md text-sm font-medium",
            "hover:bg-gray-700 hover:text-white"
        ]
        
        if self.props.active:
            classes.extend(["bg-gray-900", "text-white"])
        else:
            classes.extend(["text-gray-300"])
            
        if self.props.class_name:
            classes.append(self.props.class_name)
            
        attrs = {
            'href': self.props.href,
            'class': ' '.join(classes)
        }
        
        if self.props.id:
            attrs['id'] = self.props.id
            
        content = self.text
        if self.props.icon:
            content = f'<i class="fas fa-{self.props.icon} mr-2"></i>{content}'
            
        return self.generator.generate_element('a', content=content, attributes=attrs)

@dataclass
class NavBarProps(ComponentProps):
    """Navigation bar properties."""
    class_name: Optional[str] = None
    id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    brand: str = "Brand"
    brand_href: str = "/"
    dark: bool = True
    fixed: bool = True

class NavBar(Component):
    """Navigation bar component."""
    
    def __init__(self, items: List[NavItem], props: Optional[NavBarProps] = None):
        super().__init__(props or NavBarProps(brand="Brand"))
        self.items = items
        self.props: NavBarProps = self.props
        
    def render(self) -> str:
        nav_classes = [
            "bg-gray-800" if self.props.dark else "bg-white",
            "fixed w-full z-10 top-0" if self.props.fixed else ""
        ]
        
        if self.props.class_name:
            nav_classes.append(self.props.class_name)
            
        # Brand section
        brand = self.generator.generate_element(
            'a',
            content=self.props.brand,
            attributes={
                'href': self.props.brand_href,
                'class': 'text-white font-bold text-xl'
            }
        )
        
        # Items section
        items_html = '\n'.join(item.render() for item in self.items)
        items_container = self.generator.generate_element(
            'div',
            content=items_html,
            attributes={'class': 'flex space-x-4'}
        )
        
        # Main container
        container = self.generator.generate_element(
            'div',
            content=f'{brand}\n{items_container}',
            attributes={
                'class': 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16'
            }
        )
        
        return self.generator.generate_element(
            'nav',
            content=container,
            attributes={
                'class': ' '.join(nav_classes)
            } if not self.props.id else {
                'class': ' '.join(nav_classes),
                'id': self.props.id
            }
        )
