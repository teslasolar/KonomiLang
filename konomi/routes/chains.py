"""
Chain API Routes

This module handles API routes for executing chained programs
and complex operations.
"""
from flask import jsonify, request
from konomi.utils.performance import measure_performance

def setup_chain_routes(app, program_library):
    """
    Set up chain API routes for the application.
    
    Args:
        app: Flask application instance
        program_library: ProgramLibrary instance
    """
    
    @app.route('/api/v1/chains/analyze-code-size', methods=['POST'])
    @measure_performance(threshold=2.0)  # Code analysis might take longer
    def analyze_code_size():
        """Analyze code size and complexity."""
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        directory = request.json.get('directory')
        if not directory:
            return jsonify({'success': False, 'error': 'Directory parameter is required'}), 400
        
        try:
            result = program_library.code_analyzer(directory)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/v1/chains/modularize-function', methods=['POST'])
    @measure_performance(threshold=3.0)  # Function modularization is computationally intensive
    def modularize_function():
        """Modularize a large function."""
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        function_code = request.json.get('function_code')
        if not function_code:
            return jsonify({'success': False, 'error': 'Function code parameter is required'}), 400
        
        try:
            result = program_library.code_modularizer(function_code)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/v1/chains/generate-tests', methods=['POST'])
    @measure_performance(threshold=2.0)  # Test generation can be time-consuming
    def generate_tests():
        """Generate tests for modularized code."""
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        original_code = request.json.get('original_code')
        modularized_code = request.json.get('modularized_code')
        if not original_code or not modularized_code:
            return jsonify({'success': False, 'error': 'Both original and modularized code parameters are required'}), 400
        
        try:
            result = program_library.test_generator(original_code, modularized_code)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
