"""
Code Execution Routes

This module handles code execution routes for both web interface
and API endpoints with consistent error handling and responses.
"""
from flask import Blueprint, request
from konomi.errors import KonomiError
from konomi.interpreter import Interpreter
from konomi.chained_programs import ProgramLibrary
from konomi.web.routes.base import APIRouter

bp = Blueprint('execution', __name__)

class ExecutionRouter(APIRouter):
    """Handles all code execution related routes."""
    
    def __init__(self, blueprint: Blueprint):
        super().__init__(blueprint)
        self.interpreter = Interpreter()
        self.program_library = ProgramLibrary(self.interpreter)
        self.setup_routes()
    
    def setup_routes(self):
        """Initialize all execution routes."""
        self.route('/execute', methods=['POST'], endpoint='web_execute')(self.execute)
        self.route('/api/v1/execute', methods=['POST'], endpoint='api_execute')(self.api_execute)
        self.route('/api/v1/status', methods=['GET'], endpoint='api_status')(self.api_status)
        self.route('/api/v1/variables', methods=['GET'], endpoint='api_variables')(self.api_variables)
    
    def execute(self):
        """Execute Konomi code from web interface."""
        code = request.form.get('code', '')
        try:
            result = self.interpreter.execute(code)
            return self.success_response({'result': result})
        except KonomiError as e:
            return self.error_response(str(e))
    
    def api_execute(self):
        """Execute Konomi code via API."""
        if not request.is_json:
            return self.error_response('Content-Type must be application/json')
        
        code = request.json.get('code')
        if not code:
            return self.error_response('Code parameter is required')
        
        try:
            result = self.interpreter.execute(code)
            return self.success_response({
                'result': result,
                'variables': self.interpreter.variables
            })
        except KonomiError as e:
            return self.error_response(str(e))
    
    def api_status(self):
        """Get interpreter status."""
        return self.success_response({
            'status': 'running',
            'version': '1.0',
            'active_variables': len(self.interpreter.variables)
        })
    
    def api_variables(self):
        """Get all defined variables."""
        return self.success_response({
            'variables': self.interpreter.variables
        })

# Initialize router
router = ExecutionRouter(bp)
