from ply import yacc
import src.lexer as lexer
import src.syntaxTree as node


class Parser(object):
    def __init__(self):
        self.lexer = lexer.Lexer()
        self.lexer.build()

    tokens = lexer.Lexer.tokens

    precedence = (
        ('left', 'ADD', 'SUB'),
        ('left', 'MUL', 'DIV'),
        ('left', 'POW')
    )

    def p_command(self, p):
        """command : equation
                    | solve
                    | differentiate"""
        print(p[1])
        p[0] = node.Command("command", [p[1]])

    def p_equation(self, p):
        """equation : equation expression
                    | expression"""

        if len(p) == 3:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    def p_expression(self, p):
        """expression : expression1
                    | expression ADD expression1
                    | expression SUB expression1
                    """

        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = node.BinExpr(p[2], p[1], p[3])

    def p_expression1(self, p):
        """expression1 : expression2
                | expression1 MUL expression2
                | expression1 DIV expression2"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = node.BinExpr(p[2], p[1], p[3])

    def p_expression2(self, p):
        """expression2 : expression3
                | expression2 POW expression3"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = node.BinExpr(p[2], p[1], p[3])

    def p_expression3(self, p):
        """expression3 : LP expression RP
                    | VAR
                    | NUM
                    """

        if len(p) == 2:
            if isinstance(p[1], float):
                p[0] = node.NumExpr("number", p[1])
            else:
                p[0] = node.VarExpr("variable", p[1])

        else:
            p[0] = p[2]

    def p_trig_factor(self, p):
        """expression3 : trig"""
        p[0] = p[1]

    def p_trig_expression(self, p):
        """trig : SIN LP expression RP
                    | COS LP expression RP
                    | TG LP expression RP
                    | CTG LP expression RP"""

        p[0] = node.TrigExpr(p[1], p[3])

    def p_solve_expression(self, p):
        """solve : SOLVE FOR LP vars RP EQ LP nums RP equation"""

        print(p)
        p[0] = node.SolveExpr(p[4], p[8], p[10])

    def p_vars(self, p):
        """vars : vars VAR
                | VAR"""

        if len(p) == 2:
            p[0] = [node.VarExpr("variable", p[1])]
        else:
            p[0] = p[1] + [node.VarExpr("variable", p[2])]

    def p_nums(self, p):
        """nums : nums NUM
                | NUM"""

        if len(p) == 2:
            p[0] = [node.NumExpr("number", p[1])]
        else:
            p[0] = p[1] + [node.NumExpr("number", p[2])]

    def p_differentiate(self, p):
        """differentiate : DIFFERENTIATE equation OVER VAR"""

        p[0] = node.DiffExpr(p[2], node.VarExpr("variable", p[4]))

    def p_error(self, p):
        if p:
            print("Syntax error at token", p.type)
        else:
            print("Syntax error at EOF")

