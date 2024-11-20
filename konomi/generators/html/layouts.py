"""
HTML Layout Components
Provides reusable layout components for structuring web pages
"""
from typing import List, Optional
from dataclasses import dataclass
from .components import Component, ComponentProps

@dataclass
class GridProps(ComponentProps):
    """Grid layout properties."""
    columns: int = 12
    gap: int = 4
    rows: Optional[int] = None
    responsive: bool = True

class Grid(Component):
    """Grid layout component."""
    
    def __init__(self, children: List[str], props: Optional[GridProps] = None):
        super().__init__(props or GridProps())
        self.children = children
        self.props: GridProps = self.props
        
    def render(self) -> str:
        classes = [
            "grid",
            f"gap-{self.props.gap}",
            f"grid-cols-{self.props.columns}"
        ]
        
        if self.props.responsive:
            classes.extend([
                "grid-cols-1",
                "sm:grid-cols-2",
                f"lg:grid-cols-{self.props.columns}"
            ])
            
        if self.props.rows:
            classes.append(f"grid-rows-{self.props.rows}")
            
        if self.props.class_name:
            classes.append(self.props.class_name)
            
        attrs = {'class': ' '.join(classes)}
        if self.props.id:
            attrs['id'] = self.props.id
            
        return self.generator.generate_element(
            'div',
            content='\n'.join(self.children),
            attributes=attrs
        )

@dataclass
class FlexProps(ComponentProps):
    """Flex layout properties."""
    direction: str = "row"  # row, column
    justify: str = "start"  # start, center, end, between, around
    align: str = "start"    # start, center, end, stretch
    wrap: bool = False

class Flex(Component):
    """Flex layout component."""
    
    JUSTIFY = {
        "start": "justify-start",
        "center": "justify-center",
        "end": "justify-end",
        "between": "justify-between",
        "around": "justify-around"
    }
    
    ALIGN = {
        "start": "items-start",
        "center": "items-center",
        "end": "items-end",
        "stretch": "items-stretch"
    }
    
    def __init__(self, children: List[str], props: Optional[FlexProps] = None):
        super().__init__(props or FlexProps())
        self.children = children
        self.props: FlexProps = self.props
        
    def render(self) -> str:
        classes = ["flex"]
        
        # Direction
        classes.append(
            "flex-col" if self.props.direction == "column" else "flex-row"
        )
        
        # Justify content
        classes.append(self.JUSTIFY.get(self.props.justify, self.JUSTIFY["start"]))
        
        # Align items
        classes.append(self.ALIGN.get(self.props.align, self.ALIGN["start"]))
        
        # Wrap
        if self.props.wrap:
            classes.append("flex-wrap")
            
        if self.props.class_name:
            classes.append(self.props.class_name)
            
        attrs = {'class': ' '.join(classes)}
        if self.props.id:
            attrs['id'] = self.props.id
            
        return self.generator.generate_element(
            'div',
            content='\n'.join(self.children),
            attributes=attrs
        )

@dataclass
class ContainerProps(ComponentProps):
    """Container layout properties."""
    max_width: str = "default"  # sm, md, lg, xl, default
    padding: bool = True
    center: bool = True

class Container(Component):
    """Container layout component."""
    
    MAX_WIDTHS = {
        "sm": "max-w-screen-sm",
        "md": "max-w-screen-md",
        "lg": "max-w-screen-lg",
        "xl": "max-w-screen-xl",
        "default": "max-w-7xl"
    }
    
    def __init__(self, content: str, props: Optional[ContainerProps] = None):
        super().__init__(props or ContainerProps())
        self.content = content
        self.props: ContainerProps = self.props
        
    def render(self) -> str:
        classes = [
            self.MAX_WIDTHS.get(self.props.max_width, self.MAX_WIDTHS["default"])
        ]
        
        if self.props.padding:
            classes.extend(["px-4", "sm:px-6", "lg:px-8"])
        if self.props.center:
            classes.append("mx-auto")
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
