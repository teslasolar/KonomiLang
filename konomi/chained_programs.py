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
