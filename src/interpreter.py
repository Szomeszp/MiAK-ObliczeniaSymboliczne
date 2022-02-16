import sympy
import src.syntaxTree as syntaxTree
from src.visit import on, when


class Interpreter():
    @on("node")
    def visit(self, node):
        return "EMPTY"

    @when(syntaxTree.Command)
    def visit(self, node):
        for i in node.command:
            print(i.accept(self))

    @when(syntaxTree.VarExpr)
    def visit(self, node):
        return sympy.symbols(node.val)

    @when(syntaxTree.NumExpr)
    def visit(self, node):
        return node.val

    @when(syntaxTree.BinExpr)
    def visit(self, node):
        leftVal = node.left.accept(self)
        rightVal = node.right.accept(self)

        if node.op == "+":
            return sympy.simplify(leftVal) + sympy.simplify(rightVal)
        elif node.op == "-":
            return sympy.simplify(leftVal) - sympy.simplify(rightVal)
        elif node.op == "*":
            return sympy.simplify(leftVal) * sympy.simplify(rightVal)
        elif node.op == "/":
            return sympy.simplify(leftVal) / sympy.simplify(rightVal)
        elif node.op == "^":
            return sympy.simplify(leftVal) ** sympy.simplify(rightVal)
        elif node.op == "=":
            pass

        return None

    @when(syntaxTree.SolveExpr)
    def visit(self, node):
        equation = node.equation.accept(self)
        varDict = {}

        for i, j in zip(node.variables, node.values):
            varDict[i.accept(self)] = j.accept(self)

        return equation.evalf(subs=varDict)

    @when(syntaxTree.TrigExpr)
    def visit(self, node):
        equation = node.equation.accept(self)

        if node.function == "sin":
            return sympy.functions.sin(equation)
        elif node.function == "cos":
            return sympy.functions.cos(equation)
        elif node.function == "tg":
            return sympy.functions.tan(equation)
        elif node.function == "ctg":
            return sympy.functions.cot(equation)

    @when(syntaxTree.DiffExpr)
    def visit(self, node):
        function = node.function.accept(self)

        return sympy.diff(function, node.variables.accept(self))

    @when(syntaxTree.IntegrateExpr)
    def visit(self, node):
        function = node.function.accept(self)

        if node.start is None or node.end is None:
            return sympy.integrate(function, node.variable.accept(self))
        else:
            return sympy.integrate(function, (node.variable.accept(self), node.start.accept(self), node.end.accept(self)))

    @when(syntaxTree.LimitExpr)
    def visit(self, node):
        function = node.function.accept(self)

        if node.side is not None:
            if node.side == "left":
                return sympy.limit(function, node.variable.accept(self), node.value.accept(self), dir='-')
            elif node.side == "right":
                return sympy.limit(function, node.variable.accept(self), node.value.accept(self), dir='+')
        else:
            return sympy.limit(function, node.variable.accept(self), node.value.accept(self))