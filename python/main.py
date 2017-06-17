from Lexer import Lexer
from Parser import Parser

with open("source.pa") as fd:
    text = fd.read()

lexer = Lexer(text)
parser = Parser(lexer)
tree = parser.parse()
print(tree)
