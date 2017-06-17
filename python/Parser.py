from ASTNodes import *


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.constant_type_list = ("int",)
        self.variable_type_list = self.constant_type_list + ("array_define",)
        self.function_return_type_list = self.variable_type_list + ("void",)
        self.logic_operations = ("and", "or")
        self.compare_operations = ("morethan", "lessthan", "moreequal", "lessequal")
        self.add_and_sub = ("add", "sub")
        self.mul_and_div = ("mul", "div")
        self.block_nodes = ("ConditionBranchNode", "BlockNode", "LoopNode")

    # parse the whole program and generate an abstract syntax tree
    def parse(self):
        return self.program()

    # if token is None eat current token otherwise eat the given token
    def eat(self, token=None):
        if token is None:
            self.lexer.eat(self.lexer.current_token)
        else:
            self.lexer.eat(token)

    def getReserveToken(self, name):
        return self.lexer.getReserveToken(name)

    def currentToken(self):
        return self.lexer.current_token

    def program(self):
        funcs = []
        while self.lexer.current_token.type in self.function_return_type_list:
            func = self.functionDefine()
            funcs.append(func)

        return ProgramNode(funcs)

    def functionDefine(self):
        return_type = self.lexer.current_token.type
        self.eat()

        if self.lexer.current_token.type == "id":
            function_name = self.lexer.current_token.value
        else:
            raise Exception("Syntax Error")
        self.eat()

        self.lexer.eat(self.lexer.getReserveToken("lparen"))
        parameters = self.functionParameters()
        self.lexer.eat(self.lexer.getReserveToken("rparen"))
        block = self.block()

        return FunctionDefineNode(return_type, function_name, parameters, block)

    def functionParameters(self):
        result = []

        while self.currentToken().type in self.variable_type_list:
            if self.currentToken().type == "array_define":
                result.append(self.arrayDecleOrDefine())
            else:
                var_type = self.lexer.current_token.type
                self.lexer.eat(self.lexer.current_token)
                var_name = self.lexer.current_token.value
                self.lexer.eat(self.lexer.current_token)

                result.append(VarDeclNode(var_type, var_name))

            try:
                self.lexer.eat(self.lexer.getReserveToken("comma"))
            except:
                break

        return result

    def block(self):
        result = []

        self.lexer.eat(self.lexer.getReserveToken("lbrace"))
        statement = self.statement()
        if statement is None:
            return []

        result.append(statement)
        pre_catogory = statement.category
        while (self.lexer.current_token.type == "semi") or pre_catogory in self.block_nodes:
            if pre_catogory not in self.block_nodes:
                self.eat()
            statement = self.statement()
            if statement is None:
                break
            result.append(statement)
            pre_catogory = statement.category

        self.lexer.eat(self.lexer.getReserveToken("rbrace"))

        return result

    # parse every statement which can be if structure with several branches
    # or loop structure or variable assignment or function call
    # or variables' definition
    def statement(self):
        if self.lexer.current_token.type in self.variable_type_list:
            if self.currentToken().type is "array_define":
                return self.arrayDecleOrDefine()
            else:
                return self.varDecl()
        elif self.lexer.current_token.value == "while":
            return self.loop()
        elif self.lexer.current_token.type == "id":
            left = self.arrayCall()
            if self.currentToken().type == "assign":
                self.eat(self.getReserveToken("assign"))
                right = self.expr()
                return AssignNode(left, right)
            return left
        elif self.lexer.current_token.type == "if":
            return self.conditionBranch()
        elif self.currentToken().type is "return":
            self.eat()
            return ReturnNode(self.expr())

        return None

    def arrayDecleOrDefine(self):
        self.eat()
        if self.currentToken().type in self.variable_type_list:
            array_type = self.currentToken().type
        else:
            raise Exception("Syntax Error")

        self.eat()
        self.eat(self.getReserveToken("rparen"))

        if self.currentToken().type is "id":
            array_name = self.currentToken().value
            self.eat()
        else:
            raise Exception("Syntax Error")

        if self.currentToken().type is "lparen":
            self.eat()
            if self.currentToken().type is "int":
                array_size = self.currentToken().value
                self.eat()
                self.eat(self.getReserveToken("rparen"))

                return ArrayDefineNode(array_type, array_name, array_size)
            else:
                raise Exception("Syntax Error")

        return ArrayDeclareNode(array_type, array_name)

    def varDecl(self):
        var_type = self.lexer.current_token.type
        self.eat()
        var_name = self.lexer.current_token.value
        self.eat()

        result = []
        result.append(VarDeclNode(var_type, var_name))

        while self.lexer.current_token.type == "comma":
            self.eat()
            var_name = self.lexer.current_token.value
            self.eat()
            result.append(VarDeclNode(var_type, var_name))

        if len(result) is 1:
            return result[0]
        else:
            return MultipleVarDeclNode(result)

    def expr(self):
        return self.logicExpr()

    def logicExpr(self):
        logic_left = self.compareExpr()
        while self.lexer.current_token.type in self.logic_operations:
            logic_op = self.lexer.current_token.value
            self.lexer.eat(self.lexer.current_token)
            logic_right = self.compareExpr()

            logic_left = LogicExprNode(logic_left, logic_op, logic_right)

        return logic_left

    def compareExpr(self):
        compare_left = self.arithmeticExpr()
        while self.lexer.current_token.type in self.compare_operations:
            compare_op = self.lexer.current_token.value
            self.lexer.eat(self.lexer.current_token)
            compare_right = self.compareExpr()

            compare_left = LogicExprNode(compare_left, compare_op, compare_right)

        return compare_left

    def arithmeticExpr(self):
        left = self.term()
        while self.lexer.current_token.type in self.add_and_sub:
            op = self.lexer.current_token.value
            self.lexer.eat(self.lexer.current_token)
            right = self.term()

            left = ArithmeticExprNode(left, op, right)

        return left

    def term(self):
        left = self.factor()
        while self.lexer.current_token.type in self.mul_and_div:
            op = self.lexer.current_token.value
            self.lexer.eat(self.lexer.current_token)
            right = self.factor()

            left = ArithmeticExprNode(left, op, right)

        return left

    def factor(self):
        current_type = self.lexer.current_token.type

        if self.lexer.current_token.type == "lparen":
            self.lexer.eat(self.lexer.current_token)
            result = self.expr()
            self.lexer.eat(self.lexer.reserve_tokens.get("rparen"))

            return result
        elif self.lexer.current_token.type in self.add_and_sub:
            return self.unaryOp()
        elif current_type == "id":
            return self.arrayCall()
        elif current_type in self.constant_type_list:
            cur_token = self.currentToken()
            self.eat()
            return ConstantNode(current_type, cur_token.value)
        else:
            return None

    def arrayCall(self):
        left = self.functionCall()
        if self.currentToken().type is "lbracket":
            self.eat()
            index = self.arithmeticExpr()
            self.eat(self.getReserveToken("rbracket"))

            return ArrayCallNode(left, index)

        return left

    def functionCall(self):
        var = self.variableCall()
        if self.currentToken().type is "lparen":
            self.eat()
            parameters = []
            while self.currentToken().type is not "rparen":
                parameters.append(self.expr())
                if self.currentToken().type is not "comma":
                    break

                self.eat()

            self.eat(self.getReserveToken("rparen"))

            return FunctionCallNode(var.name, parameters)
        return var

    def variableCall(self):
        cur = self.currentToken()
        self.eat()

        return VarCallNode(cur.value)

    def unaryOp(self):
        op = self.lexer.current_token.value
        self.lexer.eat(self.lexer.current_token)

        if self.lexer.current_token.value in self.add_and_sub:
            result = UnaryNode(op, self.unaryOp())
        else:
            result = UnaryNode(op, self.factor())

        return result

    def loop(self):
        self.lexer.eat(self.lexer.getReserveToken("while"))
        self.lexer.eat(self.lexer.getReserveToken("lparen"))
        condition = self.expr()
        self.lexer.eat(self.lexer.getReserveToken("rparen"))
        block = self.block()

        return LoopNode(condition, block)

    def assign(self, name):
        self.eat()
        expr = self.expr()

        return AssignNode(name, expr)

    def conditionBranch(self):
        branch_list = []

        self.lexer.eat(self.lexer.reserve_tokens.get("if"))
        self.lexer.eat(self.lexer.reserve_tokens.get("lparen"))
        condition = self.expr()
        self.lexer.eat(self.lexer.reserve_tokens.get("rparen"))
        block = self.block()

        branch_list.append([condition, block])
        while self.lexer.current_token.type == "elif":
            self.lexer.eat(self.lexer.getReserveToken("elif"))
            self.lexer.eat(self.lexer.reserve_tokens.get("lparen"))
            condition = self.expr()
            self.lexer.eat(self.lexer.reserve_tokens.get("rparen"))
            block = self.block()

            branch_list.append([condition, block])

        if self.lexer.current_token.type == "else":
            self.lexer.eat(self.lexer.getReserveToken("else"))
            else_block = self.block()
        else:
            else_block = None

        return ConditionBranchNode(branch_list, else_block)