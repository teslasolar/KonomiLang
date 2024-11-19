import os
from openai import OpenAI
from .lexer import Lexer, TokenType
from .parser import Parser, VariableDeclaration, AskCommand, BinaryOp, Number, String, Identifier, IfStatement, TryCatch
from .errors import RuntimeError

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def visit_variabledeclaration(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value
        return f"Variable {node.name} set to: {value}"

    def visit_askcommand(self, node):
        try:
            prompt = self.visit(node.prompt) if not isinstance(node.prompt, str) else node.prompt
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"AI Error: {str(e)}")

    def visit_binaryop(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op == TokenType.PLUS:
            return left + right
        elif node.op == TokenType.MINUS:
            return left - right
        elif node.op == TokenType.MULTIPLY:
            return left * right
        elif node.op == TokenType.DIVIDE:
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif node.op == TokenType.EQUALS_EQUALS:
            return left == right
        elif node.op == TokenType.GREATER:
            return left > right
        elif node.op == TokenType.LESS:
            return left < right
        else:
            raise RuntimeError(f"Unknown operator: {node.op}")

    def visit_number(self, node):
        return node.value

    def visit_string(self, node):
        return node.value

    def visit_identifier(self, node):
        if node.name not in self.variables:
            raise RuntimeError(f"Variable '{node.name}' is not defined")
        return self.variables[node.name]

    def visit_ifstatement(self, node):
        condition = self.visit(node.condition)
        
        if condition:
            results = []
            for statement in node.if_body:
                results.append(self.visit(statement))
            return '\n'.join(results)
        elif node.else_body:
            results = []
            for statement in node.else_body:
                results.append(self.visit(statement))
            return '\n'.join(results)
        return ""

    def visit_trycatch(self, node):
        try:
            results = []
            for statement in node.try_body:
                results.append(self.visit(statement))
            return '\n'.join(results)
        except Exception as e:
            results = []
            for statement in node.catch_body:
                results.append(self.visit(statement))
            return '\n'.join(results)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__.lower()}'
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise RuntimeError(f"No visitor found for {type(node).__name__}")
        return visitor(node)

    def execute(self, code):
        try:
            lexer = Lexer(code)
            parser = Parser(lexer)
            statements = parser.parse()
            
            results = []
            for statement in statements:
                result = self.visit(statement)
                if result is not None:
                    results.append(str(result))
            
            return '\n'.join(results)
        except Exception as e:
            raise RuntimeError(str(e))
