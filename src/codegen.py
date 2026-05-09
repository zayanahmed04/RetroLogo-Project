
import turtle

class CodeGenerator:
    def __init__(self, symbols):
        self.symbols = symbols
        self.t = turtle.Turtle()
        self.screen = turtle.Screen()

    def eval_expr(self, expr):
        if isinstance(expr, int):
            return expr

        if expr[0] == 'VAR':
            return self.symbols[expr[1]]

        op = expr[0]
        left = self.eval_expr(expr[1])
        right = self.eval_expr(expr[2])

        if op == 'PLUS':
            return left + right

        if op == 'MINUS':
            return left - right

        if op == 'MUL':
            return left * right

        if op == 'DIV':
            return left // right

    def execute(self, ast):
        for stmt in ast:
            self.run(stmt)

        self.screen.mainloop()

    def run(self, node):
        kind = node[0]

        if kind == 'LET':
            return

        if kind == 'FORWARD':
            self.t.forward(self.eval_expr(node[1]))

        elif kind == 'BACKWARD':
            self.t.backward(self.eval_expr(node[1]))

        elif kind == 'LEFT':
            self.t.left(self.eval_expr(node[1]))

        elif kind == 'RIGHT':
            self.t.right(self.eval_expr(node[1]))

        elif kind == 'CIRCLE':
            self.t.circle(self.eval_expr(node[1]))

        elif kind == 'PENUP':
            self.t.penup()

        elif kind == 'PENDOWN':
            self.t.pendown()

        elif kind == 'REPEAT':
            count = self.eval_expr(node[1])

            for _ in range(count):
                for stmt in node[2]:
                    self.run(stmt)
