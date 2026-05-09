
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
            self.check_expr(node[2])
            self.symbol_table[name] = 'INT'

        elif kind in ['FORWARD', 'BACKWARD', 'LEFT', 'RIGHT', 'CIRCLE']:
            self.check_expr(node[1])

        elif kind == 'REPEAT':
            self.check_expr(node[1])

            for stmt in node[2]:
                self.visit(stmt)

    def check_expr(self, expr):
        if isinstance(expr, int):
            return

        if expr[0] == 'VAR':
            name = expr[1]

            if name not in self.symbol_table:
                raise NameError(f"Undefined variable '{name}'")

            return

        self.check_expr(expr[1])
        self.check_expr(expr[2])
