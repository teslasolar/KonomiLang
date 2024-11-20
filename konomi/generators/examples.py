"""
Example implementations of HTML and SVG generation with animations
"""
from .html_generator import HTMLGenerator
from .svg_generator import SVGGenerator
import math

def generate_example_card() -> str:
    """Generate an example card component using HTMLGenerator."""
    html_gen = HTMLGenerator()
    
    card_style = """
    .card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 16px;
        max-width: 300px;
    }
    .card-title { font-size: 1.5em; margin-bottom: 8px; }
    .card-content { color: #666; }
    """
    
    card_content = html_gen.generate_container(
        "div",
        [
            html_gen.generate_element("h2", "Example Card", {"class": "card-title"}),
            html_gen.generate_element(
                "p", 
                "This is an example card generated using HTMLGenerator.",
                {"class": "card-content"}
            )
        ],
        {"class": "card"}
    )
    
    return html_gen.generate_document("Example Card", card_content, card_style)

def generate_example_chart() -> str:
    """Generate an example animated bar chart using SVGGenerator."""
    svg_gen = SVGGenerator(300, 200)
    
    # Add background
    svg_gen.add_rect(0, 0, 300, 200, {"fill": "#f8f9fa"})
    
    # Add animated bars
    data = [50, 80, 30, 90, 60]
    bar_width = 40
    spacing = 20
    
    for i, value in enumerate(data):
        x = 40 + i * (bar_width + spacing)
        height = value
        y = 180 - height
        
        # Add bar with animation
        bar_id = f"bar-{i}"
        svg_gen.add_rect(
            x, y, bar_width, height,
            {"fill": "#4C6EF5", "stroke": "#364FC7"},
            id=bar_id
        )
        
        # Add height animation
        svg_gen.add_animation(
            bar_id, "height", 2,
            {
                "0": {"height": "0"},
                "100": {"height": str(height)}
            }
        )
        
        # Add value label
        svg_gen.add_text(
            x + bar_width/2, y - 5,
            str(value),
            {"text-anchor": "middle", "fill": "#495057", "font-size": "12px"}
        )
    
    # Add axis lines
    svg_gen.add_line(30, 180, 290, 180, {"stroke": "#212529", "stroke-width": "1"})
    svg_gen.add_line(30, 20, 30, 180, {"stroke": "#212529", "stroke-width": "1"})
    
    return svg_gen.generate()

def generate_animated_loader() -> str:
    """Generate an animated loading spinner."""
    svg_gen = SVGGenerator(100, 100)
    
    # Add central circle
    svg_gen.add_circle(50, 50, 30, 
                      {"fill": "none", "stroke": "#4C6EF5", "stroke-width": "4"},
                      id="loader")
    
    # Add rotation animation
    svg_gen.add_transform_animation(
        "loader", "rotate",
        "0 50 50", "360 50 50", 2
    )
    
    return svg_gen.generate()

def generate_animated_path() -> str:
    """Generate an animation along a path."""
    svg_gen = SVGGenerator(300, 200)
    
    # Create a curved path
    path = "M20,100 C90,0 210,0 280,100"
    
    # Add the path itself (visible but not animated)
    svg_gen.defs.append(f'<path id="motion-path" d="{path}" stroke="#ddd" stroke-width="2" fill="none"/>')
    
    # Add animated circle
    svg_gen.add_circle(0, 0, 10, 
                      {"fill": "#4C6EF5"},
                      id="moving-circle")
    
    # Add path animation
    svg_gen.add_path_animation("moving-circle", path, 3)
    
    return svg_gen.generate()

def generate_pulse_animation() -> str:
    """Generate a pulsing circle animation."""
    svg_gen = SVGGenerator(200, 200)
    
    # Add pulsing circle
    svg_gen.add_circle(100, 100, 50,
                      {"fill": "#4C6EF5", "opacity": "0.8"},
                      id="pulse")
    
    # Add scale animation
    svg_gen.add_transform_animation(
        "pulse", "scale",
        "1 1", "1.2 1.2", 1
    )
    
    # Add opacity animation
    svg_gen.add_animation(
        "pulse", "opacity", 1,
        {
            "0": {"opacity": "0.8"},
            "50": {"opacity": "0.4"},
            "100": {"opacity": "0.8"}
        }
    )
    
    return svg_gen.generate()

def generate_interactive_animations() -> str:
    """Generate an example with interactive SVG animations."""
    from konomi.generators.svg.core import SVGGenerator
    from konomi.generators.svg.animations import AnimationManager
    
    svg_gen = SVGGenerator(300, 200)
    anim_manager = AnimationManager()
    
    # Add background
    svg_gen.add_element(
        f'<rect x="0" y="0" width="300" height="200" fill="#f8f9fa"/>'
    )
    
    # Add interactive circle that scales on hover
    svg_gen.add_element(
        f'<circle cx="75" cy="100" r="30" fill="#4C6EF5" cursor="pointer" id="hover-circle"/>'
    )
    svg_gen.add_definition(
        anim_manager.create_transform_animation(
            "hover-circle", "mouseover", "scale",
            "1 1", "1.5 1.5", 0.3, "ease-out"
        )
    )
    svg_gen.add_definition(
        anim_manager.create_transform_animation(
            "hover-circle", "mouseout", "scale",
            "1.5 1.5", "1 1", 0.3, "ease-out"
        )
    )
    
    # Add interactive rectangle that rotates on click
    svg_gen.add_element(
        f'<rect x="150" y="70" width="60" height="60" fill="#FA5252" cursor="pointer" id="click-rect"/>'
    )
    svg_gen.add_definition(
        anim_manager.create_transform_animation(
            "click-rect", "click", "rotate",
            "0 30 30", "360 30 30", 1, "ease-in-out"
        )
    )
    
    # Add morphing path
    path1 = "M250,70 Q280,100 250,130"
    path2 = "M250,70 Q220,100 250,130"
    svg_gen.add_element(
        f'<path d="{path1}" stroke="#40C057" stroke-width="4" fill="none" id="morph-path" cursor="pointer"/>'
    )
    svg_gen.add_definition(
        anim_manager.create_morph_animation(
            "morph-path", path1, path2, 1, "mouseover", "ease-in-out"
        )
    )
    svg_gen.add_definition(
        anim_manager.create_morph_animation(
            "morph-path", path2, path1, 1, "mouseout", "ease-in-out"
        )
    )
    
    return svg_gen.generate()

def generate_components_example():
    """Generate an example page using the component library."""
    from .html.components import Button, ButtonProps, Input, InputProps, Card, CardProps, Alert, AlertProps
    from .html.layouts import Container, ContainerProps, Grid, GridProps, Flex, FlexProps
    from .html.forms import Form, FormProps, FormGroup, FormGroupProps, Select, SelectProps
    
    # Create a button
    button_props = ButtonProps(
        variant="primary",
        size="medium",
        class_name="mr-4"
    )
    primary_button = Button("Click Me", button_props)
    
    # Create an input
    input_props = InputProps(
        type="text",
        placeholder="Enter your name",
        required=True
    )
    text_input = Input(input_props)
    
    # Create a form group
    form_group_props = FormGroupProps(
        label="Username",
        help_text="Enter your username",
        required=True
    )
    form_group = FormGroup(text_input.render(), form_group_props)
    
    # Create a select
    select_props = SelectProps(
        options=[
            {"value": "1", "label": "Option 1"},
            {"value": "2", "label": "Option 2"},
            {"value": "3", "label": "Option 3"}
        ],
        placeholder="Select an option"
    )
    select = Select(select_props)
    
    # Create a form
    form_props = FormProps(method="post", action="/submit")
    form = Form([form_group.render(), select.render(), primary_button.render()], form_props)
    
    # Create a card
    card_props = CardProps(padding="normal", shadow="medium", hover_effect=True)
    card = Card(form.render(), card_props)
    
    # Create an alert
    alert_props = AlertProps(type="info", dismissible=True)
    alert = Alert("This is an example of the component library", alert_props)
    
    # Create a grid layout
    grid_props = GridProps(columns=2, gap=4)
    grid = Grid([card.render(), card.render()], grid_props)
    
    # Create a flex layout
    flex_props = FlexProps(direction="column", justify="center", align="center")
    flex = Flex([alert.render(), grid.render()], flex_props)
    
    # Create a container
    container_props = ContainerProps(max_width="lg", padding=True, center=True)
    container = Container(flex.render(), container_props)
    
    return container.render()