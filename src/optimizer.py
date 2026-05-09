import re


class Optimizer:
    BIN_OP_RE = re.compile(r"^(\w+) = (-?\d+) ([\+\-\*/]) (-?\d+)$")
    CONST_ASSIGN_RE = re.compile(r"^(\w+) = (-?\d+)$")
    ASSIGN_RE = re.compile(r"^(\w+) = ")

    def optimize(self, instructions):
        previous = None
        current = list(instructions)
        while previous != current:
            previous = current
            current = self.constant_fold(current)
            current = self.propagate_constants(current)
        return self.eliminate_dead_code(current)

    def constant_fold(self, instructions):
        result = []
        for ins in instructions:
            m = self.BIN_OP_RE.match(ins)
            if not m:
                result.append(ins)
                continue

            target, left, op, right = m.groups()
            left, right = int(left), int(right)

            if op == '/' and right == 0:
                result.append(ins)
                continue

            value = {'+': left + right,
                     '-': left - right,
                     '*': left * right,
                     '/': left // right if right else 0}[op]
            result.append(f"{target} = {value}")
        return result

    def propagate_constants(self, instructions):
        assignment_counts = {}
        for ins in instructions:
            m = self.ASSIGN_RE.match(ins)
            if m:
                assignment_counts[m.group(1)] = assignment_counts.get(m.group(1), 0) + 1

        constants = {}
        for ins in instructions:
            m = self.CONST_ASSIGN_RE.match(ins)
            if m and assignment_counts.get(m.group(1)) == 1 and m.group(1).startswith('t'):
                constants[m.group(1)] = m.group(2)

        if not constants:
            return instructions

        result = []
        for ins in instructions:
            assign = self.ASSIGN_RE.match(ins)
            if assign and assign.group(1) in constants and ins == f"{assign.group(1)} = {constants[assign.group(1)]}":
                result.append(ins)
                continue

            replaced = ins
            for name, value in constants.items():
                replaced = re.sub(rf"(?<![A-Za-z0-9_])({name})(?![A-Za-z0-9_])", value, replaced)
            result.append(replaced)
        return result

    def eliminate_dead_code(self, instructions):
        used = set()
        for ins in instructions:
            assign = self.ASSIGN_RE.match(ins)
            tokens = re.findall(r"\b[A-Za-z_]\w*\b", ins)
            if assign:
                tokens = [t for t in tokens if t != assign.group(1) or t in ins.split('=', 1)[1]]
            used.update(tokens)

        result = []
        for ins in instructions:
            m = self.ASSIGN_RE.match(ins)
            if m and m.group(1).startswith('t') and m.group(1) not in used:
                continue
            result.append(ins)
        return result
