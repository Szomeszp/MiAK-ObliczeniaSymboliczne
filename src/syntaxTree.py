class Node(object):
    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit(self)

class Command(Node):
    def __init__(self, type, command, args=None):
        super().__init__()
        self.type = type
        self.command = command
        self.args = args


class VarExpr(Node):
    def __init__(self, type, val):
        super().__init__()
        self.type = type
        self.val = val

class NumExpr(Node):
    def __init__(self, type, val):
        super().__init__()
        self.type = type
        self.val = val

class BinExpr(Node):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

class SolveExpr(Node):
    def __init__(self, variables, values, equation):
        super().__init__()
        self.variables = variables
        self.values = values
        self.equation = equation

class TrigExpr(Node):
    def __init__(self, function, equation):
        super().__init__()
        self.function = function
        self.equation = equation

class DiffExpr(Node):
    def __init__(self, function, variables):
        super().__init__()
        self.function = function
        self.variables = variables

