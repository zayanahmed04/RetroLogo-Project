
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, ast):
        for stmt in ast:
            self.visit(stmt)

    def visit(self, node):
        kind = node[0]

        if kind == 'LET':
            name = node[1]
            value = self.eval_expr(node[2])
            self.symbol_table[name] = value

        elif kind in ['FORWARD', 'BACKWARD', 'LEFT', 'RIGHT', 'CIRCLE']:
            self.eval_expr(node[1])

        elif kind == 'REPEAT':
            self.eval_expr(node[1])

            for stmt in node[2]:
                self.visit(stmt)

    def eval_expr(self, expr):
        if isinstance(expr, int):
            return expr

        if expr[0] == 'VAR':
            name = expr[1]

            if name not in self.symbol_table:
                raise NameError(f"Undefined variable '{name}'")

            return self.symbol_table[name]

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
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left // right
