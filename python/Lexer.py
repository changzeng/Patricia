from Token import Token
from collections import OrderedDict


class Lexer(object):
    def __init__(self, text):
        self.reserve_tokens = OrderedDict()
        self.reserve_words = OrderedDict()
        self.reserve_symbols = OrderedDict()
        self._initReserveTokens()

        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]
        self.text_length = len(text)

        self.getNextToken()

    def _initReserveTokens(self):
        self.reserve_words["while"] = Token("while", "while")
        self.reserve_words["if"] = Token("if", "if")
        self.reserve_words["elif"] = Token("elif", "elif")
        self.reserve_words["else"] = Token("else", "else")
        self.reserve_words["int"] = Token("int", "int")
        self.reserve_words["void"] = Token("void", "void")
        self.reserve_words["return"] = Token("return", "return")

        self.reserve_symbols["lparen"] = Token("lparen", "(")
        self.reserve_symbols["rparen"] = Token("rparen", ")")
        self.reserve_symbols["array_define"] = Token("array_define", "array(")
        self.reserve_symbols["comma"] = Token("comma", ",")
        self.reserve_symbols["lbrace"] = Token("lbrace", "{")
        self.reserve_symbols["rbrace"] = Token("rbrace", "}")
        self.reserve_symbols["lbracket"] = Token("lbracket", "[")
        self.reserve_symbols["rbracket"] = Token("rbracket", "]")
        self.reserve_symbols["moreequal"] = Token("moreequal", ">=")
        self.reserve_symbols["lessequal"] = Token("lessequal", "<=")
        self.reserve_symbols["morethan"] = Token("morethan", ">")
        self.reserve_symbols["lessthan"] = Token("lessthan", "<")
        self.reserve_symbols["equal"] = Token("equal", "==")
        self.reserve_symbols["assign"] = Token("assign", "=")
        self.reserve_symbols["semi"] = Token("semi", ";")
        self.reserve_symbols["or"] = Token("or", "||")
        self.reserve_symbols["and"] = Token("and", "&&")
        self.reserve_symbols["plus"] = Token("add", "+")
        self.reserve_symbols["sub"] = Token("sub", "-")
        self.reserve_symbols["mul"] = Token("mul", "*")
        self.reserve_symbols["div"] = Token("div", "/")

        self.reserve_tokens.update(self.reserve_words)
        self.reserve_tokens.update(self.reserve_symbols)

    def getReserveToken(self, name):
        return self.reserve_tokens[name]

    def eat(self, token):
        if self.current_token.type == token.type:
            self.advance(token=token)
            self.getNextToken()
        else:
            raise Exception('Syntax Error')

    # advance d char or advance a token
    def advance(self, d=1, token=None):
        if token is not None:
            d = len(str(token.value))
        for i in range(d):
            self.pos += 1
            if self.pos < self.text_length:
                self.current_char = self.text[self.pos]
            else:
                return False

        return True

    # skip white space tab and line-breaker
    def skipSpace(self):
        if self.pos >= self.text_length:
            return False

        while self.current_char == ' ' or self.current_char == '\n' or self.current_char == '\t':
            if not self.advance():
                return False

        return True

    def skipComment(self):
        while self.current_char != '\n':
            if not self.advance():
                return False

        return self.skipSpace()

    def getInteger(self):
        result = ""
        offset = 0
        while self.text[self.pos + offset].isdigit():
            result += self.text[self.pos + offset]
            offset += 1

        return Token("int", int(result))

    def getVar(self):
        result = ""
        offset = 0
        while self.text[self.pos+offset].isalnum():
            result += self.text[self.pos+offset]
            offset += 1

        return Token("id", result)

    def getNextToken(self):
        if not self.skipSpace():
            self.current_token = Token("eof", None)
            return self.current_token

        if self.text[self.pos:self.pos+2] == '//':
            if not self.skipComment():
                self.current_token = Token("eof", None)
                return self.current_token

        for key, token in self.reserve_symbols.items():
            if self.text[self.pos:self.pos + len(token.value)] == token.value:
                self.current_token = token
                return self.current_token

        for key, token in self.reserve_words.items():
            if self.text[self.pos:self.pos + len(token.value)] == token.value:
                tmp = self.text[self.pos + len(token.value)].isalnum()
                if self.text[self.pos + len(token.value)].isalnum() or self.text[self.pos + len(token.value)] is "_":
                    break
                else:
                    self.current_token = token
                    return self.current_token

        if self.current_char.isdigit():
            self.current_token = self.getInteger()
            return self.current_token

        if self.current_char.isalpha():
            self.current_token = self.getVar()
            return self.current_token

        print(self.current_char)

        raise Exception('Syntax Error')

    def getAllTokens(self):
        while self.skipSpace():
            print(self.getNextToken())
            self.eat(self.current_token)
