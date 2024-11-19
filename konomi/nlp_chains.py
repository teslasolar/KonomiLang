from .interpreter import Interpreter

class NLPChains:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def grammar_checker(self, text):
        steps = [
            f'let input_text = """{text}"""',
            'let grammar_check = ask "Check this text for grammar errors and provide corrections: " + input_text',
            'let explanations = ask "Explain each grammar correction in detail"',
            'let suggestions = ask "Provide writing style improvements"'
        ]
        return self.execute_chain(steps)

    def paraphraser(self, text, style="formal"):
        steps = [
            f'let input_text = """{text}"""',
            f'let style = "{style}"',
            'let paraphrase = ask "Paraphrase this text in a " + style + " style: " + input_text',
            'let alternatives = ask "Provide two alternative paraphrased versions"',
            'let explanations = ask "Explain the differences between the versions"'
        ]
        return self.execute_chain(steps)

    def text_simplifier(self, text, target_level="middle school"):
        steps = [
            f'let input_text = """{text}"""',
            f'let level = "{target_level}"',
            'let simplified = ask "Simplify this text for a " + level + " reading level: " + input_text',
            'let vocabulary = ask "Identify and explain any potentially difficult terms"',
            'let check = ask "Verify the simplified version maintains the original meaning"'
        ]
        return self.execute_chain(steps)

    def contextual_thesaurus(self, text, word):
        steps = [
            f'let input_text = """{text}"""',
            f'let target_word = "{word}"',
            'let synonyms = ask "Provide contextually appropriate synonyms for \'" + target_word + "\' in this text: " + input_text',
            'let usage = ask "Explain how each synonym would change the meaning or tone"',
            'let examples = ask "Provide example sentences using each synonym"'
        ]
        return self.execute_chain(steps)

    def style_analyzer(self, text):
        steps = [
            f'let input_text = """{text}"""',
            'let style_analysis = ask "Analyze the writing style of this text: " + input_text',
            'let tone = ask "Identify the tone and emotional undertones"',
            'let patterns = ask "Identify recurring linguistic patterns and stylistic devices"',
            'let recommendations = ask "Suggest style improvements based on the analysis"'
        ]
        return self.execute_chain(steps)

    def execute_chain(self, steps):
        results = []
        variables = {}
        
        for step in steps:
            try:
                result = self.interpreter.execute(step)
                results.append(result)
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
