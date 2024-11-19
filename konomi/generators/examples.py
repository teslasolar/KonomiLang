"""
Example implementations of HTML and SVG generation
"""
from .html_generator import HTMLGenerator
from .svg_generator import SVGGenerator

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
    """Generate an example bar chart using SVGGenerator."""
    svg_gen = SVGGenerator(300, 200)
    
    # Add background
    svg_gen.add_rect(0, 0, 300, 200, {"fill": "#f8f9fa"})
    
    # Add bars
    data = [50, 80, 30, 90, 60]
    bar_width = 40
    spacing = 20
    
    for i, value in enumerate(data):
        x = 40 + i * (bar_width + spacing)
        height = value
        y = 180 - height
        
        svg_gen.add_rect(
            x, y, bar_width, height,
            {"fill": "#4C6EF5", "stroke": "#364FC7"}
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
