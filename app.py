from flask import Flask, render_template, request, jsonify, send_from_directory
from konomi.interpreter import Interpreter
from konomi.errors import KonomiError
from konomi.konomi_lexer import KonomiLexer
import markdown
import os
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
