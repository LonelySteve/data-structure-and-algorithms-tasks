class Node(object):
    NAME = 'node'

    def __repr__(self):
        return f"<{self.__class__.NAME} {', '.join([k + '=' + str(v) for k, v in self.__dict__.items()])}>"


class Number(Node):
    NAME = 'number'

    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError()
        self.value = value


class Variable(Node):
    """变元"""
    NAME = 'variable'

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError()
        self.value = value


# 这个项目只有二元操作符
class Operator(Node):
    NAME = 'operator'
    OP = ''

    def __init__(self, l_value, r_value):
        self.l_value = l_value
        self.r_value = r_value

    def __repr__(self):
        return f"<{self.__class__.NAME} '{self.__class__.OP}' {', '.join([k + '=' + str(v) for k, v in self.__dict__.items()])} > "


def calc_result(self):
    raise NotImplementedError()


class Add(Operator):
    """加法"""
    OP = '+'

    def calc_result(self):
        raise NotImplementedError()


class Sub(Operator):
    """减法"""
    OP = '-'

    def calc_result(self):
        raise NotImplementedError()


class Mul(Operator):
    """乘法"""
    OP = '*'

    def calc_result(self):
        raise NotImplementedError()


class Pow(Operator):
    """幂"""
    OP = '^'

    def calc_result(self):
        raise NotImplementedError()


class SubItem(Node):
    def __init__(self, id: Variable,exponent: Number = None):
        pass


class Item(Node):
    """项"""

    def __init__(self, coefficient,  ):
        pass


class Expression(Node):
    def __init__(self, add_op):
        pass
