"""
Code Execution Routes

This module handles code execution routes for both web interface
and API endpoints.
"""
from flask import Blueprint, jsonify, request
from konomi.errors import KonomiError
from konomi.interpreter import Interpreter
from konomi.chained_programs import ProgramLibrary

bp = Blueprint('execution', __name__)
interpreter = Interpreter()
program_library = ProgramLibrary(interpreter)

@bp.route('/execute', methods=['POST'])
def execute():
    """Execute Konomi code from web interface."""
    code = request.form.get('code', '')
    try:
        result = interpreter.execute(code)
        return jsonify({'success': True, 'result': result})
    except KonomiError as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/api/v1/execute', methods=['POST'])
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

@bp.route('/api/v1/status', methods=['GET'])
def api_status():
    """Get interpreter status."""
    return jsonify({
        'success': True,
        'status': 'running',
        'version': '1.0',
        'active_variables': len(interpreter.variables)
    })

@bp.route('/api/v1/variables', methods=['GET'])
def api_variables():
    """Get all defined variables."""
    return jsonify({
        'success': True,
        'variables': interpreter.variables
    })
