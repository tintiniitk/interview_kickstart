VariablesMap = dict[str, float]

class Expression:
    def eval(self, m: VariablesMap) -> float:
        raise ValueError("Generic operand evaluation not supported")
    def simplify(self) -> 'Expression':
        raise ValueError("Generic operand evaluation not supported")

class Number(Expression):
    value: float = 0
    def __init__(self, value: float):
        self.value = value
    def eval(self, m: VariablesMap) -> float:
        return self.value
    def simplify(self) -> Expression:
        print(f"simplify not implemented yet !!")
        return self

class Variable(Expression):
    name: str = "x"
    def __init__(self, name: str):
        self.name = name
    def eval(self, m: VariablesMap) -> float:
        if self.name in m:
            return m[self.name]
        raise ValueError(f"Evaluating unknown variable {self.name} with variable-map {m}")
    def simplify(self) -> Expression:
        print(f"simplify not implemented yet !!")
        return self

class BinaryOperation:
    def execute(self, operand1: Expression, operand2: Expression, m: VariablesMap) -> float:
        raise ValueError("Generic operation evaluation not supported for operands {operand1}, {operand2}")
class PlusOperation(BinaryOperation):
    def execute(self, operand1: Expression, operand2: Expression, m: VariablesMap) -> float:
        return operand1.eval(m) + operand2.eval(m)
class MultiplyOperation(BinaryOperation):
    def execute(self, operand1: Expression, operand2: Expression, m: VariablesMap) -> float:
        return operand1.eval(m) * operand2.eval(m)

class BinaryExpression(Expression):
    operand1: Expression
    operand2: Expression
    op: BinaryOperation
    def __init__(self, op: BinaryOperation, operand1: Expression, operand2: Expression):
        self.operand1 = operand1
        self.operand2 = operand2
        self.op = op
    def eval(self, m: VariablesMap) -> float:
        return self.op.execute(self.operand1, self.operand2, m)
    def simplify(self) -> Expression:
        print(f"simplify not implemented yet !!")
        return self

def Evaluate(expression: str):
    raise ValueError("Evaluate utility not implemented yet")

def main():
    plus = PlusOperation()
    into = MultiplyOperation()
    expr = BinaryExpression(plus, BinaryExpression(plus, BinaryExpression(into, Number(3), Variable('x')), BinaryExpression(into, Number(2), Variable('y'))), Number(-1))
    print(f"expr={expr}, eval = {expr.eval({'x': 1, 'y': 2})}")

if __name__ == "__main__":
    main()
