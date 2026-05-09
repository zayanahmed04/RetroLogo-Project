import re

TOKEN_SPECIFICATION = [
    ('NUMBER',    r'\d+'),
    ('START',     r'START\b'),      # \b added to all keywords
    ('END',       r'END\b'),
    ('LET',       r'LET\b'),
    ('FORWARD',   r'FORWARD\b'),
    ('BACKWARD',  r'BACKWARD\b'),
    ('LEFT',      r'LEFT\b'),
    ('RIGHT',     r'RIGHT\b'),
    ('REPEAT',    r'REPEAT\b'),
    ('CIRCLE',    r'CIRCLE\b'),
    ('PENUP',     r'PENUP\b'),
    ('PENDOWN',   r'PENDOWN\b'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('PLUS',      r'\+'),
    ('MINUS',     r'-'),
    ('MUL',       r'\*'),
    ('DIV',       r'/'),
    ('ASSIGN',    r'='),
    ('IDENTIFIER',r'[A-Za-z_][A-Za-z0-9_]*'),
    ('NEWLINE',   r'\n'),
    ('SKIP',      r'[ \t]+'),
    ('MISMATCH',  r'.')
]

TOK_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"{self.type}:{self.value}"

def tokenize(code):          # accepts a code string
    tokens = []
    line_num = 1

    for mo in re.finditer(TOK_REGEX, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NEWLINE':
            line_num += 1
            continue
        if kind == 'SKIP':
            continue
        if kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character '{value}' at line {line_num}")

        tokens.append(Token(kind, value, line_num))

    return tokens

#print(tokenize("START\nFORWARD 10\nEND"))