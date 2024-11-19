"""
Core API Routes

This module handles core language operations like code execution,
status checks, and variable management.
"""
from flask import jsonify, request
from konomi.errors import KonomiError

def setup_core_routes(app, interpreter):
    """
    Set up core API routes for the application.
    
    Args:
        app: Flask application instance
        interpreter: Konomi interpreter instance
    """
    
    @app.route('/api/v1/execute', methods=['POST'])
    def api_execute():
        """Execute Konomi code via API."""
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        code = request.json.get('code')
        if not code:
            return jsonify({'success': False, 'error': 'Code parameter is required'}), 400
        
        try:
            result = interpreter.execute(code)
            return jsonify({
                'success': True,
                'result': result,
                'variables': interpreter.variables
            })
        except KonomiError as e:
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500

    @app.route('/api/v1/status', methods=['GET'])
    def api_status():
        """Get interpreter status."""
        return jsonify({
            'success': True,
            'status': 'running',
            'version': '1.0',
            'active_variables': len(interpreter.variables)
        })

    @app.route('/api/v1/variables', methods=['GET'])
    def api_variables():
        """Get all defined variables."""
        return jsonify({
            'success': True,
            'variables': interpreter.variables
        })
