from .interpreter import Interpreter

class ChainedProgram:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def execute_chain(self, steps):
        results = []
        variables = {}
        
        for step in steps:
            try:
                result = self.interpreter.execute(step)
                results.append(result)
                # Update variables after each step
                variables.update(self.interpreter.variables)
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'partial_results': results,
                    'variables': variables
                }
        
        return {
            'success': True,
            'results': results,
            'variables': variables
        }

class ProgramLibrary:
    def __init__(self, interpreter):
        self.chain = ChainedProgram(interpreter)

    def code_analyzer(self, directory):
        steps = [
            f'let dir = "{directory}"',
            'let large_functions = ask "Scan this directory and identify all functions over 150 lines: " + dir',
            'let complexity = ask "Analyze the complexity and dependencies of these functions"',
            'let metadata = ask "Generate metadata including size, complexity metrics, and dependency graph"',
            'let recommendations = ask "Provide initial recommendations for breaking down these functions"'
        ]
        return self.chain.execute_chain(steps)

    def code_modularizer(self, function_code):
        steps = [
            f'let code = """{function_code}"""',
            'let flow_analysis = ask "Analyze the logical flow and identify distinct responsibilities in this function: " + code',
            'let break_points = ask "Suggest logical break points where the function can be split"',
            'let modular_version = ask "Generate a modularized version with smaller, focused functions"',
            'let documentation = ask "Generate documentation for the new modular structure"'
        ]
        return self.chain.execute_chain(steps)

    def test_generator(self, original_code, modularized_code):
        steps = [
            f'let original = """{original_code}"""',
            f'let modular = """{modularized_code}"""',
            'let test_cases = ask "Generate comprehensive test cases covering both versions: \nOriginal:\n" + original + "\nModular:\n" + modular',
            'let edge_cases = ask "Identify and create test cases for edge cases and boundary conditions"',
            'let equivalence_tests = ask "Generate tests to verify functional equivalence between versions"'
        ]
        return self.chain.execute_chain(steps)

    def backup_manager(self, code_data):
        steps = [
            f'let code = """{code_data}"""',
            'let backup_entry = ask "Create a backup entry with metadata and versioning information for: " + code',
            'let timestamp = ask "Generate timestamp and tracking information"',
            'let rollback_plan = ask "Create a rollback strategy for this code version"'
        ]
        return self.chain.execute_chain(steps)

    def code_replacer(self, validated_code):
        steps = [
            f'let code = """{validated_code}"""',
            'let dependency_check = ask "Verify all dependencies and references for the new code: " + code',
            'let replacement_plan = ask "Generate a safe replacement strategy"',
            'let reference_updates = ask "Identify all references that need to be updated"',
            'let verification_steps = ask "Create verification steps for the replacement process"'
        ]
        return self.chain.execute_chain(steps)

    def content_analyzer(self, text):
        steps = [
            f'let input_text = "{text}"',
            'let summary = ask "Summarize this text in 3 sentences: " + input_text',
            'let keywords = ask "Extract 5 key topics from this text: " + input_text',
            'let sentiment = ask "Analyze the sentiment of this text: " + input_text'
        ]
        return self.chain.execute_chain(steps)
    
    def code_reviewer(self, code):
        steps = [
            f'let code = "{code}"',
            'let review = ask "Review this code and identify potential issues: " + code',
            'let improvements = ask "Suggest specific improvements for the code: " + code',
            'let security = ask "Identify any security concerns in this code: " + code'
        ]
        return self.chain.execute_chain(steps)
    
    def business_analyzer(self, description):
        steps = [
            f'let business_idea = "{description}"',
            'let analysis = ask "Analyze this business idea and provide key insights: " + business_idea',
            'let market = ask "Identify the target market and potential competitors: " + business_idea',
            'let risks = ask "What are the main risks and challenges for this business? " + business_idea',
            'let recommendations = ask "Provide actionable recommendations for this business: " + business_idea'
        ]
        return self.chain.execute_chain(steps)
    
    def language_tutor(self, text, target_language):
        steps = [
            f'let original_text = "{text}"',
            f'let target_language = "{target_language}"',
            'let translation = ask "Translate this text to " + target_language + ": " + original_text',
            'let pronunciation = ask "Provide pronunciation guide for: " + translation',
            'let grammar = ask "Explain the grammar rules used in this translation"',
            'let examples = ask "Provide 3 similar examples in " + target_language'
        ]
        return self.chain.execute_chain(steps)
    
    def story_developer(self, premise):
        steps = [
            f'let story_premise = "{premise}"',
            'let characters = ask "Create 3 interesting characters for this story: " + story_premise',
            'let plot = ask "Develop a plot outline based on these characters: " + characters',
            'let dialogue = ask "Write a key dialogue scene between two main characters"',
            'let ending = ask "Suggest 3 possible endings for this story"'
        ]
        return self.chain.execute_chain(steps)

    def sentiment_analyzer(self, text):
        steps = [
            f'let input_text = "{text}"',
            'let sentiment = ask "Perform detailed sentiment analysis on this text, including emotional tones: " + input_text',
            'let key_phrases = ask "Extract key phrases that indicate sentiment: " + input_text',
            'let suggestions = ask "Suggest ways to improve the tone if negative, or maintain if positive: " + input_text'
        ]
        return self.chain.execute_chain(steps)

    def text_classifier(self, text, categories):
        steps = [
            f'let input_text = "{text}"',
            f'let categories = "{categories}"',
            'let classification = ask "Classify this text into the following categories: " + categories + "\nText: " + input_text',
            'let confidence = ask "Provide confidence scores for each category classification"',
            'let explanation = ask "Explain the reasoning behind the classification"'
        ]
        return self.chain.execute_chain(steps)

    def entity_recognizer(self, text):
        steps = [
            f'let input_text = "{text}"',
            'let entities = ask "Extract and categorize all named entities (people, organizations, locations, etc.) from this text: " + input_text',
            'let relationships = ask "Identify relationships between the extracted entities"',
            'let context = ask "Provide additional context for the main entities identified"'
        ]
        return self.chain.execute_chain(steps)

    def document_summarizer(self, text, summary_type="general"):
        steps = [
            f'let input_text = "{text}"',
            f'let summary_type = "{summary_type}"',
            'let summary = ask "Create a " + summary_type + " summary of this document: " + input_text',
            'let key_points = ask "Extract the main points and arguments from the document"',
            'let structure = ask "Analyze the document structure and organization"'
        ]
        return self.chain.execute_chain(steps)

    def data_validator(self, data, schema):
        steps = [
            f'let input_data = "{data}"',
            f'let schema = "{schema}"',
            'let validation = ask "Validate this data against the schema and identify any issues: \nSchema: " + schema + "\nData: " + input_data',
            'let suggestions = ask "Suggest corrections for any validation issues found"',
            'let format = ask "Recommend optimal data format and structure"'
        ]
        return self.chain.execute_chain(steps)

    def data_analyzer(self, data):
        steps = [
            f'let input_data = "{data}"',
            'let patterns = ask "Identify patterns and trends in this data: " + input_data',
            'let statistics = ask "Calculate key statistical measures and insights"',
            'let correlations = ask "Identify correlations between different data points"',
            'let anomalies = ask "Detect and explain any anomalies in the data"'
        ]
        return self.chain.execute_chain(steps)

    def component_builder(self, specifications):
        steps = [
            f'let specs = """{specifications}"""',
            'let structure = ask "Analyze these component specifications and suggest an appropriate component structure: " + specs',
            'let component_code = ask "Generate the component code based on this structure: " + structure',
            'let metadata = ask "Generate metadata including component dependencies, version, and requirements"',
            'let documentation = ask "Generate comprehensive documentation for this component"'
        ]
        return self.chain.execute_chain(steps)

    def component_validator(self, component):
        steps = [
            f'let component = """{component}"""',
            'let best_practices = ask "Validate this component against best practices and coding standards: " + component',
            'let syntax_check = ask "Perform a detailed syntax analysis and identify potential issues"',
            'let structure_review = ask "Review the component structure and organization, suggest improvements"',
            'let security_audit = ask "Identify any security concerns or vulnerabilities in the component"'
        ]
        return self.chain.execute_chain(steps)

    def component_optimizer(self, component, feedback):
        steps = [
            f'let component = """{component}"""',
            f'let feedback = """{feedback}"""',
            'let analysis = ask "Analyze the component and feedback to identify optimization opportunities: " + component + "\nFeedback: " + feedback',
            'let optimizations = ask "Generate specific optimization recommendations"',
            'let improved_code = ask "Apply the optimizations and generate improved component code"',
            'let performance_notes = ask "Provide notes on expected performance improvements"'
        ]
        return self.chain.execute_chain(steps)

    def component_integration_tester(self, component, context):
        steps = [
            f'let component = """{component}"""',
            f'let context = """{context}"""',
            'let integration_analysis = ask "Analyze how this component integrates with the given context: " + component + "\nContext: " + context',
            'let dependency_check = ask "Verify all dependencies and their compatibility"',
            'let test_cases = ask "Generate comprehensive test cases for integration testing"',
            'let compatibility_report = ask "Generate a detailed compatibility report"'
        ]
        return self.chain.execute_chain(steps)

    def component_error_loop(self, specifications):
        steps = [
            f'let specs = """{specifications}"""',
            'let initial_build = ask "Generate initial component based on specifications: " + specs',
            'let validation = ask "Validate the component against quality standards"',
            'let optimization_cycle = ask "Identify and apply necessary optimizations"',
            'let quality_metrics = ask "Calculate quality metrics and compare against thresholds"',
            'let final_report = ask "Generate final quality assessment report"'
        ]
        return self.chain.execute_chain(steps)

    def media_analyzer(self, media_url, analysis_type="full"):
        steps = [
            f'let url = "{media_url}"',
            f'let type = "{analysis_type}"',
            'let content_analysis = ask "Analyze the media content at: " + url + " focusing on " + type',
            'let context = ask "Provide contextual information and metadata about this media"',
            'let recommendations = ask "Generate content recommendations based on this media"'
        ]
        return self.chain.execute_chain(steps)

    def tutorial_generator(self, topic, skill_level):
        steps = [
            f'let topic = "{topic}"',
            f'let level = "{skill_level}"',
            'let outline = ask "Create an interactive tutorial outline for " + topic + " at " + level + " level"',
            'let content = ask "Generate detailed tutorial content with examples and exercises"',
            'let assessment = ask "Create assessment questions and practical exercises"',
            'let feedback = ask "Generate adaptive feedback responses for common mistakes"'
        ]
        return self.chain.execute_chain(steps)

    def knowledge_graph_builder(self, domain, concepts):
        steps = [
            f'let domain = "{domain}"',
            f'let concepts = "{concepts}"',
            'let entities = ask "Extract key entities and relationships from: " + concepts + " in the domain of " + domain',
            'let relationships = ask "Map relationships and dependencies between these entities"',
            'let hierarchy = ask "Create a hierarchical structure of concepts"',
            'let visualization = ask "Generate a textual representation of the knowledge graph"'
        ]
        return self.chain.execute_chain(steps)

    def code_generator(self, specifications, language):
        steps = [
            f'let specs = """{specifications}"""',
            f'let lang = "{language}"',
            'let design = ask "Design software architecture based on specifications: " + specs + " in " + lang',
            'let implementation = ask "Generate implementation code following the design"',
            'let documentation = ask "Create comprehensive documentation for the generated code"',
            'let tests = ask "Generate unit tests for the implementation"'
        ]
        return self.chain.execute_chain(steps)

    def pattern_recognizer(self, data_sample, pattern_type):
        steps = [
            f'let data = """{data_sample}"""',
            f'let type = "{pattern_type}"',
            'let analysis = ask "Analyze this data to identify " + type + " patterns: " + data',
            'let patterns = ask "Extract and describe identified patterns"',
            'let insights = ask "Provide insights and implications of these patterns"',
            'let recommendations = ask "Suggest actions based on the identified patterns"'
        ]
        return self.chain.execute_chain(steps)

    def interactive_debugger(self, code, error_message):
        steps = [
            f'let code = """{code}"""',
            f'let error = "{error_message}"',
            'let analysis = ask "Analyze this code and error: " + error + "\nCode:\n" + code',
            'let explanation = ask "Explain the cause of the error in simple terms"',
            'let solution = ask "Provide step-by-step solution to fix the error"',
            'let prevention = ask "Suggest best practices to prevent similar errors"'
        ]
        return self.chain.execute_chain(steps)