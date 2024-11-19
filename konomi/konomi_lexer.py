from pygments.lexer import RegexLexer, words
from pygments.token import *

class KonomiLexer(RegexLexer):
    name = 'Konomi'
    aliases = ['konomi']
    filenames = ['*.konomi']

    tokens = {
        'root': [
            (r'\s+', Text.Whitespace),
            (words(('let', 'ask', 'if', 'else', 'try', 'catch', 'ls', 'mkdir', 'rmdir'), 
                  prefix=r'\b', suffix=r'\b'), Keyword),
            (r'[0-9]+(\.[0-9]+)?', Number),
            (r'"[^"]*"', String),
            (r'\+|\-|\*|\/|\=\=|\>|\<', Operator),
            (r'\(|\)|\{|\}', Punctuation),
            (r'[A-Za-z_][A-Za-z0-9_]*', Name.Variable),
            (r'#.*?$', Comment.Single),
        ]
    }
