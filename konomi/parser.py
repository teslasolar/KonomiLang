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

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class IfStatement(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class TryCatch(ASTNode):
    def __init__(self, try_body, catch_body):
        self.try_body = try_body
        self.catch_body = catch_body

# New AST nodes for file system operations
class ListDirectoryCommand(ASTNode):
    def __init__(self, path=None):
        self.path = path

class CreateDirectoryCommand(ASTNode):
    def __init__(self, path):
        self.path = path

class RemoveDirectoryCommand(ASTNode):
    def __init__(self, path):
        self.path = path

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
        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.TRY:
            return self.try_catch()
        elif self.current_token.type == TokenType.LS:
            return self.list_directory()
        elif self.current_token.type == TokenType.MKDIR:
            return self.create_directory()
        elif self.current_token.type == TokenType.RMDIR:
            return self.remove_directory()
        else:
            return self.expr()

    def variable_declaration(self):
        self.eat(TokenType.LET)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.EQUALS)
        value = self.expr()
        return VariableDeclaration(name, value)

    def ask_command(self):
        self.eat(TokenType.ASK)
        if self.current_token.type == TokenType.STRING:
            prompt = self.current_token.value
            self.eat(TokenType.STRING)
            return AskCommand(prompt)
        elif self.current_token.type == TokenType.IDENTIFIER:
            return AskCommand(self.expr())
        else:
            raise SyntaxError("Expected string or variable after 'ask'")

    # New methods for file system operations
    def list_directory(self):
        self.eat(TokenType.LS)
        path = None
        if self.current_token.type in (TokenType.STRING, TokenType.IDENTIFIER):
            path = self.expr()
        return ListDirectoryCommand(path)

    def create_directory(self):
        self.eat(TokenType.MKDIR)
        if self.current_token.type in (TokenType.STRING, TokenType.IDENTIFIER):
            path = self.expr()
            return CreateDirectoryCommand(path)
        raise SyntaxError("Expected path after 'mkdir'")

    def remove_directory(self):
        self.eat(TokenType.RMDIR)
        if self.current_token.type in (TokenType.STRING, TokenType.IDENTIFIER):
            path = self.expr()
            return RemoveDirectoryCommand(path)
        raise SyntaxError("Expected path after 'rmdir'")

    def if_statement(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.expr()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        if_body = []
        while self.current_token.type != TokenType.RBRACE:
            if_body.append(self.statement())
        self.eat(TokenType.RBRACE)
        
        else_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            else_body = []
            while self.current_token.type != TokenType.RBRACE:
                else_body.append(self.statement())
            self.eat(TokenType.RBRACE)
        
        return IfStatement(condition, if_body, else_body)

    def try_catch(self):
        self.eat(TokenType.TRY)
        self.eat(TokenType.LBRACE)
        try_body = []
        while self.current_token.type != TokenType.RBRACE:
            try_body.append(self.statement())
        self.eat(TokenType.RBRACE)
        
        self.eat(TokenType.CATCH)
        self.eat(TokenType.LBRACE)
        catch_body = []
        while self.current_token.type != TokenType.RBRACE:
            catch_body.append(self.statement())
        self.eat(TokenType.RBRACE)
        
        return TryCatch(try_body, catch_body)

    def expr(self):
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS, 
                                      TokenType.EQUALS_EQUALS, TokenType.GREATER, 
                                      TokenType.LESS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            elif token.type == TokenType.EQUALS_EQUALS:
                self.eat(TokenType.EQUALS_EQUALS)
            elif token.type == TokenType.GREATER:
                self.eat(TokenType.GREATER)
            elif token.type == TokenType.LESS:
                self.eat(TokenType.LESS)
            
            node = BinaryOp(node, token.type, self.term())
        
        return node

    def term(self):
        node = self.factor()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            
            node = BinaryOp(node, token.type, self.factor())
        
        return node

    def factor(self):
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            raise SyntaxError(f"Unexpected token {token.type}")
