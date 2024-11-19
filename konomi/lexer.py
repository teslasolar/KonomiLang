from enum import Enum, auto

class TokenType(Enum):
    LET = auto()
    IDENTIFIER = auto()
    EQUALS = auto()
    STRING = auto()
    NUMBER = auto()
    ASK = auto()
    IF = auto()
    ELSE = auto()
    TRY = auto()
    CATCH = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    GREATER = auto()
    LESS = auto()
    EQUALS_EQUALS = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def get_number(self):
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(result))

    def get_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        keywords = {
            'let': TokenType.LET,
            'ask': TokenType.ASK,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'try': TokenType.TRY,
            'catch': TokenType.CATCH
        }
        
        return Token(keywords.get(result, TokenType.IDENTIFIER), result)

    def get_string(self):
        result = ''
        self.advance()  # Skip opening quote
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, result)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self.get_identifier()

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char == '"':
                return self.get_string()

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUALS_EQUALS, '==')
                return Token(TokenType.EQUALS, '=')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}')

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '>':
                self.advance()
                return Token(TokenType.GREATER, '>')

            if self.current_char == '<':
                self.advance()
                return Token(TokenType.LESS, '<')

        return Token(TokenType.EOF, None)
