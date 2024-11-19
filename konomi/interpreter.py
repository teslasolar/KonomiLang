import os
from openai import OpenAI
from .lexer import Lexer
from .parser import Parser, VariableDeclaration, AskCommand
from .errors import RuntimeError

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def visit_variable_declaration(self, node):
        self.variables[node.name] = node.value
        return f"Variable {node.name} set to: {node.value}"

    def visit_ask_command(self, node):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": node.prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"AI Error: {str(e)}")

    def execute(self, code):
        lexer = Lexer(code)
        parser = Parser(lexer)
        statements = parser.parse()
        
        results = []
        for statement in statements:
            if isinstance(statement, VariableDeclaration):
                results.append(self.visit_variable_declaration(statement))
            elif isinstance(statement, AskCommand):
                results.append(self.visit_ask_command(statement))
            else:
                raise RuntimeError(f"Unknown statement type: {type(statement)}")
        
        return '\n'.join(results)
