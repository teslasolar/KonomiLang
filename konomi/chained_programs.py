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
