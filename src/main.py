from ply import yacc
from ply import lex
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

if __name__ == "__main__":
    while True:
        try:
            userInput = input("\n>>")
            if userInput == "exit":
                break
        except EOFError:
            break

        lexer = Lexer()
        lexer.build()
        lexer.input(userInput)

        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)

        parser = yacc.yacc(module=Parser())
        syntaxTree = parser.parse(userInput, lexer=Parser().lexer)

        interpreter = Interpreter()
        syntaxTree.accept(interpreter)
