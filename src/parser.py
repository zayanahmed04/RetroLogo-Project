
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current()

        if token and token.type == token_type:
            self.pos += 1
            return token

        line = token.line if token else "EOF"
        raise SyntaxError(f"Expected {token_type} at line {line}")

    def parse(self):
        self.eat('START')

        statements = []

        while self.current() and self.current().type != 'END':
            statements.append(self.statement())

        self.eat('END')
        return statements

    def statement(self):
        token = self.current()

        if token.type in ['FORWARD', 'BACKWARD', 'LEFT', 'RIGHT']:
            return self.move_statement()

        if token.type == 'CIRCLE':
            self.eat('CIRCLE')
            return ('CIRCLE', self.expression())

        if token.type == 'LET':
            return self.let_statement()

        if token.type == 'REPEAT':
            return self.repeat_statement()

        if token.type == 'PENUP':
            self.eat('PENUP')
            return ('PENUP',)

        if token.type == 'PENDOWN':
            self.eat('PENDOWN')
            return ('PENDOWN',)

        raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

    def move_statement(self):
        command = self.current().type
        self.eat(command)
        value = self.expression()
        return (command, value)

    def let_statement(self):
        self.eat('LET')
        identifier = self.eat('IDENTIFIER').value
        self.eat('ASSIGN')
        expr = self.expression()
        return ('LET', identifier, expr)

    def repeat_statement(self):
        self.eat('REPEAT')
        count = self.expression()
        self.eat('LBRACE')

        body = []

        while self.current().type != 'RBRACE':
            body.append(self.statement())

        self.eat('RBRACE')
        return ('REPEAT', count, body)

    def expression(self):
        node = self.term()

        while self.current() and self.current().type in ['PLUS', 'MINUS']:
            op = self.current().type
            self.eat(op)
            node = (op, node, self.term())

        return node

    def term(self):
        node = self.factor()

        while self.current() and self.current().type in ['MUL', 'DIV']:
            op = self.current().type
            self.eat(op)
            node = (op, node, self.factor())

        return node

    def factor(self):
        token = self.current()

        if token.type == 'NUMBER':
            return int(self.eat('NUMBER').value)

        if token.type == 'IDENTIFIER':
            return ('VAR', self.eat('IDENTIFIER').value)

        if token.type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr

        raise SyntaxError(f"Invalid expression at line {token.line}")
