
class IRGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, ast):
        for stmt in ast:
            self.visit(stmt)

        return self.instructions

    def visit(self, node):
        kind = node[0]

        if kind == 'LET':
            place = self.gen_expr(node[2])
            self.instructions.append(f"{node[1]} = {place}")

        elif kind in ['FORWARD', 'BACKWARD', 'LEFT', 'RIGHT', 'CIRCLE']:
            place = self.gen_expr(node[1])
            self.instructions.append(f"{kind} {place}")

        elif kind in ['PENUP', 'PENDOWN']:
            self.instructions.append(kind)

        elif kind == 'REPEAT':
            place = self.gen_expr(node[1])
            start = self.new_label()
            end = self.new_label()
            counter = self.new_temp()

            self.instructions.append(f"{counter} = {place}")
            self.instructions.append(f"LABEL {start}")
            self.instructions.append(f"IF {counter} <= 0 GOTO {end}")

            for stmt in node[2]:
                self.visit(stmt)

            self.instructions.append(f"{counter} = {counter} - 1")
            self.instructions.append(f"GOTO {start}")
            self.instructions.append(f"LABEL {end}")

    OP_SYMBOL = {'PLUS': '+', 'MINUS': '-', 'MUL': '*', 'DIV': '/'}

    def gen_expr(self, expr):
        if isinstance(expr, int):
            return str(expr)

        if expr[0] == 'VAR':
            return expr[1]

        op = expr[0]
        left = self.gen_expr(expr[1])
        right = self.gen_expr(expr[2])
        temp = self.new_temp()
        self.instructions.append(f"{temp} = {left} {self.OP_SYMBOL[op]} {right}")
        return temp
