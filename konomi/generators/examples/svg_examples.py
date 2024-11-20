"""
SVG example implementations
"""
from ..svg.core import SVGGenerator
from ..svg.charts import ChartGenerator

def generate_example_card() -> str:
    """Generate an example SVG card."""
    svg = SVGGenerator(200, 100)
    svg.add_element(
        '<rect width="180" height="80" x="10" y="10" '
        'rx="5" fill="white" stroke="#ccc"/>'
    )
    return svg.generate()

def generate_example_chart() -> str:
    """Generate an example chart."""
    chart = ChartGenerator(400, 300)
    data = [10, 45, 30, 25, 60, 15]
    labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    return chart.generate_bar_chart(data, labels, title="Monthly Sales")

def generate_animated_loader() -> str:
    """Generate an animated loading indicator."""
    svg = SVGGenerator(50, 50)
    svg.add_element(
        '<circle cx="25" cy="25" r="20" fill="none" '
        'stroke="#4C6EF5" stroke-width="4">'
        '<animateTransform attributeName="transform" '
        'type="rotate" from="0 25 25" to="360 25 25" '
        'dur="1s" repeatCount="indefinite"/>'
        '</circle>'
    )
    return svg.generate()

def generate_animated_path() -> str:
    """Generate a path with animation."""
    svg = SVGGenerator(200, 100)
    svg.add_element(
        '<path d="M10 50 Q100 10 190 50" stroke="#4C6EF5" '
        'fill="none" stroke-width="4">'
        '<animate attributeName="d" '
        'values="M10 50 Q100 10 190 50;'
        'M10 50 Q100 90 190 50;'
        'M10 50 Q100 10 190 50" '
        'dur="2s" repeatCount="indefinite"/>'
        '</path>'
    )
    return svg.generate()

def generate_pulse_animation() -> str:
    """Generate a pulsing circle animation."""
    svg = SVGGenerator(100, 100)
    svg.add_element(
        '<circle cx="50" cy="50" r="20" fill="#4C6EF5">'
        '<animate attributeName="r" values="20;30;20" '
        'dur="1.5s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="1;0.5;1" '
        'dur="1.5s" repeatCount="indefinite"/>'
        '</circle>'
    )
    return svg.generate()
