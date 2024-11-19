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

    @app.route('/api/v1/chains/sentiment-analysis', methods=['POST'])
    def analyze_sentiment():
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        text = request.json.get('text')
        if not text:
            return jsonify({'success': False, 'error': 'Text parameter is required'}), 400
        
        try:
            result = program_library.sentiment_analyzer(text)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/v1/chains/text-classification', methods=['POST'])
    def classify_text():
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        text = request.json.get('text')
        categories = request.json.get('categories')
        if not text or not categories:
            return jsonify({'success': False, 'error': 'Text and categories parameters are required'}), 400
        
        try:
            result = program_library.text_classifier(text, categories)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/v1/chains/entity-recognition', methods=['POST'])
    def recognize_entities():
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        text = request.json.get('text')
        if not text:
            return jsonify({'success': False, 'error': 'Text parameter is required'}), 400
        
        try:
            result = program_library.entity_recognizer(text)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/v1/chains/document-summary', methods=['POST'])
    def summarize_document():
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        text = request.json.get('text')
        summary_type = request.json.get('summary_type', 'general')
        if not text:
            return jsonify({'success': False, 'error': 'Text parameter is required'}), 400
        
        try:
            result = program_library.document_summarizer(text, summary_type)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/v1/chains/data-validation', methods=['POST'])
    def validate_data():
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        data = request.json.get('data')
        schema = request.json.get('schema')
        if not data or not schema:
            return jsonify({'success': False, 'error': 'Data and schema parameters are required'}), 400
        
        try:
            result = program_library.data_validator(data, schema)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/v1/chains/data-analysis', methods=['POST'])
    def analyze_data():
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        data = request.json.get('data')
        if not data:
            return jsonify({'success': False, 'error': 'Data parameter is required'}), 400
        
        try:
            result = program_library.data_analyzer(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/analyze-code-size', methods=['POST'])
def analyze_code_size():
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
def modularize_function():
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
def generate_tests():
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

@app.route('/api/v1/chains/backup-code', methods=['POST'])
def backup_code():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    code_data = request.json.get('code_data')
    if not code_data:
        return jsonify({'success': False, 'error': 'Code data parameter is required'}), 400
    
    try:
        result = program_library.backup_manager(code_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/replace-code', methods=['POST'])
def replace_code():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    validated_code = request.json.get('validated_code')
    if not validated_code:
        return jsonify({'success': False, 'error': 'Validated code parameter is required'}), 400
    
    try:
        result = program_library.code_replacer(validated_code)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/analyze-media', methods=['POST'])
def analyze_media():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    media_url = request.json.get('media_url')
    analysis_type = request.json.get('analysis_type', 'full')
    
    if not media_url:
        return jsonify({'success': False, 'error': 'Media URL parameter is required'}), 400
    
    try:
        result = program_library.media_analyzer(media_url, analysis_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/generate-tutorial', methods=['POST'])
def generate_tutorial():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    topic = request.json.get('topic')
    skill_level = request.json.get('skill_level', 'beginner')
    
    if not topic:
        return jsonify({'success': False, 'error': 'Topic parameter is required'}), 400
    
    try:
        result = program_library.tutorial_generator(topic, skill_level)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/build-knowledge-graph', methods=['POST'])
def build_knowledge_graph():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    domain = request.json.get('domain')
    concepts = request.json.get('concepts')
    
    if not domain or not concepts:
        return jsonify({'success': False, 'error': 'Domain and concepts parameters are required'}), 400
    
    try:
        result = program_library.knowledge_graph_builder(domain, concepts)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/generate-code', methods=['POST'])
def generate_code():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    specifications = request.json.get('specifications')
    language = request.json.get('language', 'python')
    
    if not specifications:
        return jsonify({'success': False, 'error': 'Specifications parameter is required'}), 400
    
    try:
        result = program_library.code_generator(specifications, language)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/recognize-patterns', methods=['POST'])
def recognize_patterns():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    data_sample = request.json.get('data_sample')
    pattern_type = request.json.get('pattern_type', 'general')
    
    if not data_sample:
        return jsonify({'success': False, 'error': 'Data sample parameter is required'}), 400
    
    try:
        result = program_library.pattern_recognizer(data_sample, pattern_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/debug-interactive', methods=['POST'])
def debug_interactive():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    code = request.json.get('code')
    error_message = request.json.get('error_message')
    
    if not code or not error_message:
        return jsonify({'success': False, 'error': 'Code and error message parameters are required'}), 400
    
    try:
        result = program_library.interactive_debugger(code, error_message)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/database-setup', methods=['POST'])
def setup_database():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    config = request.json.get('config')
    if not config:
        return jsonify({'success': False, 'error': 'Database configuration is required'}), 400
    
    try:
        result = program_library.database_setup(config)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/database-migration', methods=['POST'])
def migrate_database():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    schema = request.json.get('schema')
    if not schema:
        return jsonify({'success': False, 'error': 'Database schema is required'}), 400
    
    try:
        result = program_library.database_migration(schema)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/database-backup', methods=['POST'])
def backup_database():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    data = request.json.get('data')
    if not data:
        return jsonify({'success': False, 'error': 'Database data is required'}), 400
    
    try:
        result = program_library.database_backup(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/database-validate', methods=['POST'])
def validate_database():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    queries = request.json.get('queries')
    if not queries:
        return jsonify({'success': False, 'error': 'Database queries are required'}), 400
    
    try:
        result = program_library.database_validator(queries)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/chains/database-restore', methods=['POST'])
def restore_database():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    backup = request.json.get('backup')
    if not backup:
        return jsonify({'success': False, 'error': 'Backup data is required'}), 400
    
    try:
        result = program_library.database_restorer(backup)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)