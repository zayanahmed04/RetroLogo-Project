
class IRGenerator:
    def __init__(self):
        self.instructions = []

    def generate(self, ast):
        for stmt in ast:
            self.visit(stmt)

        return self.instructions

    def visit(self, node):
        kind = node[0]

        if kind == 'LET':
            self.instructions.append(f"LET {node[1]} = {node[2]}")

        elif kind in ['FORWARD', 'BACKWARD', 'LEFT', 'RIGHT', 'CIRCLE']:
            self.instructions.append(f"{kind} {node[1]}")

        elif kind == 'REPEAT':
            self.instructions.append(f"LOOP_START {node[1]}")

            for stmt in node[2]:
                self.visit(stmt)

            self.instructions.append("LOOP_END")
