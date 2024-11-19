from pygments.lexer import RegexLexer, words, include, bygroups
from pygments.token import *

class KonomiLexer(RegexLexer):
    name = 'Konomi'
    aliases = ['konomi']
    filenames = ['*.konomi']

    tokens = {
        'root': [
            (r'\s+', Text.Whitespace),
            (r'#.*?$', Comment.Single),
            (words((
                'let', 'ask', 'if', 'else', 'try', 'catch',
                'ls', 'mkdir', 'rmdir',
                'checkConsole', 'listErrors'
            ), prefix=r'\b', suffix=r'\b'), Keyword),
            (r'[0-9]+(\.[0-9]+)?', Number.Float),
            (r'"([^"\\]|\\.)*"', String.Double),
            (r'\+|\-|\*|\/|\=\=|\>|\<|\=', Operator),
            (r'\(|\)|\{|\}', Punctuation),
            (r'\b(true|false)\b', Keyword.Constant),
            (r'[A-Za-z_][A-Za-z0-9_]*', Name.Variable),
        ],
    }
