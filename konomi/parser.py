from .lexer import TokenType
from .errors import SyntaxError

class ASTNode:
    pass

class VariableDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class AskCommand(ASTNode):
    def __init__(self, prompt):
        self.prompt = prompt

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == TokenType.LET:
            return self.variable_declaration()
        elif self.current_token.type == TokenType.ASK:
            return self.ask_command()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.type}")

    def variable_declaration(self):
        self.eat(TokenType.LET)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.EQUALS)
        if self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.eat(TokenType.STRING)
        else:
            raise SyntaxError("Expected string value")
        return VariableDeclaration(name, value)

    def ask_command(self):
        self.eat(TokenType.ASK)
        prompt = self.current_token.value
        self.eat(TokenType.STRING)
        return AskCommand(prompt)
