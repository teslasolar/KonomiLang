"""
SVG Chart Routes Module

Handles routes for SVG chart generation and visualization.
"""
from flask import Blueprint
from konomi.generators.svg.charts import ChartGenerator
from konomi.web.routes.base import APIRouter

bp = Blueprint('charts', __name__)

class ChartRouter(APIRouter):
    """Handles all chart-related routes."""
    
    def __init__(self, blueprint: Blueprint):
        super().__init__(blueprint)
        self.setup_routes()
    
    def setup_routes(self):
        """Initialize all chart routes."""
        self.route('/examples/svg/charts', endpoint='svg_charts')(self.svg_charts)
        self.route('/examples/svg/interactive', endpoint='svg_interactive')(self.svg_charts)
    
    def svg_charts(self):
        """Render example SVG charts."""
        chart_gen = ChartGenerator(400, 300)
        
        # Create bar chart
        bar_data = [float(x) for x in [10, 45, 30, 25, 60, 15]]
        bar_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        bar_svg = chart_gen.generate_bar_chart(
            bar_data, bar_labels, 
            title="Monthly Sales"
        )
        
        # Create line chart
        line_data = [float(x) for x in [20, 35, 45, 30, 55, 40]]
        line_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        line_svg = chart_gen.generate_line_chart(
            line_data, line_labels,
            title="Weekly Traffic"
        )
        
        # Create pie chart
        pie_chart = ChartGenerator(400, 400)
        pie_data = [float(x) for x in [30, 20, 15, 25, 10]]
        pie_labels = ["A", "B", "C", "D", "E"]
        pie_svg = pie_chart.generate_pie_chart(
            pie_data, pie_labels,
            title="Market Share"
        )
        
        # Combine all charts
        combined_svg = f'''
        <svg width="1200" height="400" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(0,0)">{bar_svg}</g>
            <g transform="translate(400,0)">{line_svg}</g>
            <g transform="translate(800,0)">{pie_svg}</g>
        </svg>
        '''
        
        return combined_svg, 200, {'Content-Type': 'image/svg+xml'}

# Initialize router
router = ChartRouter(bp)
