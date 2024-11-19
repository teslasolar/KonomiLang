from .lexer import Lexer
from .parser import Parser
from .errors import RuntimeError

class Interpreter:
    def __init__(self):
        self.variables = {}

    def visit_variable_declaration(self, node):
        self.variables[node.name] = node.value
        return f"Variable {node.name} set to: {node.value}"

    def visit_ask_command(self, node):
        # In a real implementation, this would connect to an AI model
        return f"AI Response to: {node.prompt}"

    def execute(self, code):
        lexer = Lexer(code)
        parser = Parser(lexer)
        statements = parser.parse()
        
        results = []
        for statement in statements:
            if isinstance(statement, parser.VariableDeclaration):
                results.append(self.visit_variable_declaration(statement))
            elif isinstance(statement, parser.AskCommand):
                results.append(self.visit_ask_command(statement))
            else:
                raise RuntimeError(f"Unknown statement type: {type(statement)}")
        
        return '\n'.join(results)
