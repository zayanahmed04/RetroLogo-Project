
class Optimizer:
    def optimize(self, instructions):
        optimized = []

        for ins in instructions:
            if " + " in ins:
                try:
                    left, right = ins.split(" + ")
                    value = int(left.strip()) + int(right.strip())
                    optimized.append(str(value))
                except:
                    optimized.append(ins)
            else:
                optimized.append(ins)

        # dead code elimination
        cleaned = []

        for ins in optimized:
            if "unused" not in ins:
                cleaned.append(ins)

        return cleaned
