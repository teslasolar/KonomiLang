from flask import Flask, render_template, request, jsonify, send_from_directory
from konomi.interpreter import Interpreter
from konomi.errors import KonomiError
from konomi.konomi_lexer import KonomiLexer
import markdown
import os
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from konomi.chained_programs import ProgramLibrary  # Import ProgramLibrary

app = Flask(__name__)
interpreter = Interpreter()

# Configure Markdown extensions
markdown_extensions = [
    'fenced_code',
    'codehilite',
    'tables',
    'attr_list'
]

def highlight_code(code, language='konomi'):
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style='monokai', cssclass='highlight')
        return highlight(code, lexer, formatter)
    except:
        return code

app.jinja_env.globals.update(highlight_code=highlight_code)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    # Read and convert README.md
    with open('docs/README.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="Documentation")

@app.route('/docs/api')
def api_docs():
    # Read and convert api.md
    with open('docs/api.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="API Documentation")

@app.route('/docs/endpoints')
def endpoints_docs():
    # Read and convert endpoints.md
    with open('docs/endpoints.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="API Endpoints")

@app.route('/docs/syntax')
def syntax_docs():
    # Read and convert basic_syntax.md
    with open('docs/basic_syntax.md', 'r') as f:
        content = markdown.markdown(f.read(), extensions=markdown_extensions)
    return render_template('markdown.html', content=content, title="Basic Syntax")

@app.route('/examples')
def examples():
    return render_template('examples.html')

# Original execute endpoint for web interface
@app.route('/execute', methods=['POST'])
def execute():
    code = request.form.get('code', '')
    try:
        result = interpreter.execute(code)
        return jsonify({'success': True, 'result': result})
    except KonomiError as e:
        return jsonify({'success': False, 'error': str(e)})

# API Routes
@app.route('/api/v1/execute', methods=['POST'])
def api_execute():
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
    return jsonify({
        'success': True,
        'status': 'running',
        'version': '1.0',
        'active_variables': len(interpreter.variables)
    })

@app.route('/api/v1/variables', methods=['GET'])
def api_variables():
    return jsonify({
        'success': True,
        'variables': interpreter.variables
    })

# Initialize program library
program_library = ProgramLibrary(interpreter)  # Initialize ProgramLibrary

# Complex Chained Program Endpoints
@app.route('/api/v1/chains/analyze-content', methods=['POST'])
def analyze_content():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    text = request.json.get('text')
    if not text:
        return jsonify({'success': False, 'error': 'Text parameter is required'}), 400
    
    try:
        result = program_library.content_analyzer(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/review-code', methods=['POST'])
def review_code():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    code = request.json.get('code')
    if not code:
        return jsonify({'success': False, 'error': 'Code parameter is required'}), 400
    
    try:
        result = program_library.code_reviewer(code)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/analyze-business', methods=['POST'])
def analyze_business():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    description = request.json.get('description')
    if not description:
        return jsonify({'success': False, 'error': 'Description parameter is required'}), 400
    
    try:
        result = program_library.business_analyzer(description)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/language-tutor', methods=['POST'])
def language_tutor():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    text = request.json.get('text')
    target_language = request.json.get('target_language')
    if not text or not target_language:
        return jsonify({'success': False, 'error': 'Text and target_language parameters are required'}), 400
    
    try:
        result = program_library.language_tutor(text, target_language)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/story-developer', methods=['POST'])
def story_developer():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    premise = request.json.get('premise')
    if not premise:
        return jsonify({'success': False, 'error': 'Premise parameter is required'}), 400
    
    try:
        result = program_library.story_developer(premise)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)