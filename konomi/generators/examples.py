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
