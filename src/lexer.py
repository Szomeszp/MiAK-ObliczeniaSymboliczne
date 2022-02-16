from ply import lex


class Lexer():
    def build(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    reserved = {
        "solve": "SOLVE",
        "for": "FOR",
        "over": "OVER",
        "limit": "LIMIT",
        "at": "AT",
        "from": "FROM",
        "to": "TO",
        "differentiate": "DIFFERENTIATE",
        "integrate": "INTEGRATE",
        "variable": "VARIABLE",
        "sin": "SIN",
        "cos": "COS",
        "tg": "TG",
        "ctg": "CTG"
    }

    tokens = [
         "ADD",
         "SUB",
         "MUL",
         "DIV",
         "POW",
         "EQ",
         "NUM",
         "VAR",
         "LP",
         "RP",
         "STR"
     ] + list(reserved.values())

    t_ADD = r"\+"
    t_SUB = r"-"
    t_MUL = r"\*"
    t_DIV = r"/"
    t_POW = r"\^"
    t_EQ = r"\="
    t_LP = r"\("
    t_RP = r"\)"

    t_ignore = " \t"

    def t_NUM(self, t):
        r"\d+\.\d+|\d+"
        t.value = float(t.value)
        return t

    def t_STR(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, "VAR")
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character {t.value[0]} at line {t.lexer.lineno}")
        t.lexer.skip(1)
