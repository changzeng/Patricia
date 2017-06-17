class AST(object):
    def __init__(self, category):
        self.category = category

    def __str__(self):
        return self.category

    __repr__ = __str__


# this is the root node of the whole AST
class ProgramNode(AST):
    def __init__(self, function_list):
        super(ProgramNode, self).__init__("ProgramNode")

        self.function_list = function_list


# this is the function define node
# in this program language there has no function declaration but only function definitions
class FunctionDefineNode(AST):
    def __init__(self, func_return_type, func_name, func_parameters, func_block):
        super(FunctionDefineNode, self).__init__("FunctionDefineNode")

        self.func_return_type = func_return_type
        self.func_name = func_name
        self.func_parameters = func_parameters
        self.func_block = func_block


class VarDeclNode(AST):
    def __init__(self, var_type, var_name):
        super(VarDeclNode, self).__init__("VarDeclNode")

        self.var_type = var_type
        self.var_name = var_name


class MultipleVarDeclNode(AST):
    def __init__(self, declarations):
        super(MultipleVarDeclNode, self).__init__("MultipleVarDeclNode")

        self.declarations = declarations


class VarInitializeNode(AST):
    def __init__(self, declare, value):
        super(VarInitializeNode, self).__init__("VarInitializeNode")

        self.declare = declare
        self.value = value


class ArrayDeclareNode(AST):
    def __init__(self, array_type, array_name):
        super(ArrayDeclareNode, self).__init__("ArrayDeclareNode")

        self.array_type = array_type
        self.array_name = array_name


class ArrayDefineNode(AST):
    def __init__(self, array_type, array_name, array_size):
        super(ArrayDefineNode, self).__init__("ArrayDefineNode")

        self.array_type = array_type
        self.array_name = array_name
        self.array_size = array_size


class BlockNode(AST):
    def __init__(self, statements):
        super(BlockNode, self).__init__("BlockNode")

        self.statements = statements


class LogicExprNode(AST):
    def __init__(self, left, op, right):
        super(LogicExprNode, self).__init__("LogicExprNode")

        self.left = left
        self.op = op
        self.right = right


class CompareExprNode(AST):
    def __init__(self, left, op, right):
        super(CompareExprNode, self).__init__("CompareExprNode")

        self.left = left
        self.op = op
        self.right = right


class ArithmeticExprNode(AST):
    def __init__(self, left, op, right):
        super(ArithmeticExprNode, self).__init__("ArithmeticExprNode")

        self.left = left
        self.op = op
        self.right = right


class ConstantNode(AST):
    def __init__(self, type, value):
        super(ConstantNode, self).__init__("ConstantNode")

        self.type = type
        self.value = value


class UnaryNode(AST):
    def __init__(self, op, value):
        super(UnaryNode, self).__init__("UnaryNode")

        self.op = op
        self.value = value


class ArrayCallNode(AST):
    def __init__(self, array_name, index):
        super(ArrayCallNode, self).__init__("ArrayCallNode")

        self.array_name = array_name
        self.index = index


class FunctionCallNode(AST):
    def __init__(self, func_name, arguments):
        super(FunctionCallNode, self).__init__("FunctionCallNode")

        self.func_name = func_name
        self.arguments = arguments


class VarCallNode(AST):
    def __init__(self, name):
        super(VarCallNode, self).__init__("VarCallNode")

        self.name = name


class LoopNode(AST):
    def __init__(self, condition, block):
        super(LoopNode, self).__init__("LoopNode")

        self.condition = condition
        self.block = block


class AssignNode(AST):
    def __init__(self, var, expr):
        super(AssignNode, self).__init__("AssignNode")

        self.var = var
        self.expr = expr


class ConditionBranchNode(AST):
    def __init__(self, branch_list, else_block):
        super(ConditionBranchNode, self).__init__("ConditionBranchNode")

        self.branch_list = branch_list
        self.else_block = else_block


class ReturnNode(AST):
    def __init__(self, value):
        super(ReturnNode, self).__init__("ReturnNode")

        self.value = value
