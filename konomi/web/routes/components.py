"""
Components Routes Module

Handles routes for component previews and examples.
"""
from flask import Blueprint, jsonify, request, render_template
from konomi.generators.examples import generate_components_example
from konomi.web.routes.base import APIRouter

bp = Blueprint('components', __name__)

class ComponentsRouter(APIRouter):
    """Handles all component-related routes."""
    
    def __init__(self, blueprint: Blueprint):
        super().__init__(blueprint)
        self.setup_routes()
    
    def setup_routes(self):
        """Initialize all component routes."""
        self.route('/examples/components', endpoint='example_components')(self.example_components)
        self.route('/api/components/preview', methods=['POST'], endpoint='preview_component')(self.preview_component)
    
    def example_components(self):
        """Render example components page."""
        components_html = generate_components_example()
        return render_template('components_example.html', components=components_html)
    
    def preview_component(self):
        """Preview a component with given props."""
        try:
            if not request.is_json:
                return self.error_response('Content-Type must be application/json')
                
            component_type = request.json.get('type')
            props = request.json.get('props', {})
            
            if not component_type:
                return self.error_response('Component type is required')
            
            if component_type == 'button':
                from konomi.generators.html.components import Button, ButtonProps
                button = Button(text=props.get('text', 'Button'), props=ButtonProps(**props))
                return self.success_response({'html': button.render()})
            elif component_type == 'alert':
                from konomi.generators.html.components import Alert, AlertProps
                alert = Alert(message=props.get('message', 'Alert'), props=AlertProps(**props))
                return self.success_response({'html': alert.render()})
            
            return self.error_response('Invalid component type')
        except Exception as e:
            return self.error_response(str(e))

# Initialize router
router = ComponentsRouter(bp)
