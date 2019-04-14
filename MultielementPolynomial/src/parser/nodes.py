from copy import deepcopy

from operator import add, sub, mul, pow

_ops = {
    '+': add,
    '-': sub,
    '*': mul,
    '^': pow,
}


class Node(object):
    NAME = 'node'

    def __repr__(self):
        return f"<{self.__class__.NAME} {', '.join([k + '=' + str(v) for k, v in self.__dict__.items()])}>"

    def clone(self):
        return self.__class__()


class SingleValueNode(Node):
    """单值节点"""

    def __init__(self, value):
        self.value = value

    def clone(self):
        if hasattr(self.value, "clone"):
            copy_value = self.value.clone()
        else:
            copy_value = deepcopy(self.value)

        return self.__class__(copy_value)


class Number(SingleValueNode):
    NAME = 'number'

    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError()
        super().__init__(value)


class Variable(SingleValueNode):
    """变元"""
    NAME = 'variable'

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError()
        super().__init__(value)


# 这个项目只有二元操作符
class BinExpr(Node):
    NAME = 'binExpr'
    OP = ''

    def __init__(self, l_value, r_value):
        self.l_value = l_value
        self.r_value = r_value

    @property
    def value(self):
        return self.OP

    @property
    def op_method(self):
        return _ops[self.OP]

    def clone(self):
        if hasattr(self.l_value, "clone"):
            copy_l_value = self.l_value.clone()
        else:
            copy_l_value = deepcopy(self.l_value)

        if hasattr(self.r_value, "clone"):
            copy_r_value = self.r_value.clone()
        else:
            copy_r_value = deepcopy(self.r_value)

        return self.__class__(copy_l_value, copy_r_value)

    def __repr__(self):
        return f"<{self.__class__.NAME} '{self.__class__.OP}' " \
            f" {', '.join([k + '=' + str(v) for k, v in self.__dict__.items()])} > "


class Add(BinExpr):
    """加法"""
    OP = '+'


class Sub(BinExpr):
    """减法"""
    OP = '-'


class Mul(BinExpr):
    """乘法"""
    OP = '*'


class Pow(BinExpr):
    """幂"""
    OP = '^'


class MPExpression(object):
    """多元多项表达式"""

    def __init__(self, root_node):
        self._vars = {}
        self.root_node = root_node

        calc_stack = []
        temp_vars_stack = []

        def calc(node):
            if hasattr(node, "OP"):
                rhs = calc_stack.pop()
                lhs = calc_stack.pop()
                result = node.op_method(lhs, rhs)
                calc_stack.append(result)
            elif isinstance(node, Number):
                wrap_item = Item(node.value)
                calc_stack.append(wrap_item)
            elif isinstance(node, Variable):
                s = SubItem()
                s.append(node.value)
                temp_vars_stack.append(node.value)
                item = Item(sub_item=s)
                calc_stack.append(item)
            else:
                raise ValueError()

        after_traverse(root_node, calc)

        self._vars = set(temp_vars_stack)
        self._value = result = calc_stack[0]
        # 化简
        if isinstance(result, MultielementPolynomial):
            if result.items:
                val = result.items[0]
                for item in result.items[1:]:
                    val += item
                self._value = val
        # 如果计算结果是Item，再包装成MultielementPolynomial
        if isinstance(self._value, Item):
            self._value = MultielementPolynomial(self._value)

    @property
    def vars(self):
        return self._vars

    def get_value(self):
        return self._value


class MultielementPolynomial(Node):
    def __init__(self, *items):
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        buffer = []
        for i, item in enumerate(self.items):
            if i == 0:
                buffer.append(item)
            else:
                if item.coefficient > 0:
                    buffer.append("+")
                    buffer.append(item)
                elif item.coefficient < 0:
                    buffer.append(item)
                else:
                    # 系数为0的不显示
                    pass

        # 如果buffer为空说明表达式值为0
        if not buffer:
            buffer.append(Item(0))

        return ''.join([str(i) for i in buffer])

    def __add__(self, other):
        if isinstance(other, MultielementPolynomial):
            # 多项式和多项式相加
            items = self.items + other.items

            if items:
                result = items[0]
                for item in items[1:]:
                    result += item
                return result
        else:
            if isinstance(other, Item):
                other_item = other
            elif isinstance(other, Number):
                other_item = other.value and Item(other.value)
            elif isinstance(other, Variable):
                s = SubItem()
                s.append(other.value)
                other_item = Item(sub_item=s)
            else:
                raise ValueError()

            items = list(self.items)
            for i, item in enumerate(items):
                if item.sub_item == other_item.sub_item:
                    items[i] = item + other_item
                    break
            else:
                items.append(other_item)

        return MultielementPolynomial(*items)

    def __sub__(self, other):
        if isinstance(other, MultielementPolynomial):
            sub_items = other.items

            if sub_items:
                result = sub_items[0]
                for item in sub_items[1:]:
                    result -= item
                return result
            return MultielementPolynomial(*self.items)
        else:
            if isinstance(other, Item):
                other_item = other
            elif isinstance(other, Number):
                other_item = other.value and Item(other.value)
            elif isinstance(other, Variable):
                s = SubItem()
                s.append(other.value)
                other_item = Item(sub_item=s)
            else:
                raise ValueError()

            items = list(self.items)
            for i, item in enumerate(items):
                if item.sub_item == other_item.sub_item:
                    items[i] = item - other_item
                    break
            else:
                items.append(-other_item)

            return MultielementPolynomial(*items)

    def __mul__(self, other):
        if isinstance(other, MultielementPolynomial):
            # 多项式和多项式相乘
            items = []
            for item_1 in self.items:
                for item_2 in other.items:
                    new_item = item_1 * item_2
                    items.append(new_item)

            return MultielementPolynomial(*items)
        elif isinstance(other, (Item, Number, Variable, int, float)):
            # 项与多项式相乘
            items = []
            for item in self.items:
                new_item = item * other
                items.append(new_item)

            return MultielementPolynomial(*items)
        else:
            raise ValueError()

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            result = self
            for _ in range(power.value):
                result *= self
            return result
        else:
            raise NotImplementedError("暂不支持幂为其他类型的情况")


class Item(Node):
    """项"""

    def __init__(self, coefficient=None, sub_item=None):
        if coefficient is None:
            coefficient = 1
        self.coefficient = coefficient
        self.sub_item = sub_item or SubItem()

    def __str__(self):
        return f"{self.coefficient}{self.sub_item}"

    def __neg__(self):
        return Item(-self.coefficient, self.sub_item)

    def __add__(self, other):
        if isinstance(other, Item):
            # 合并
            if (self.sub_item == other.sub_item):
                coefficient_result = self.coefficient + other.coefficient
                return Item(coefficient_result, self.sub_item)
            return MultielementPolynomial(self, other)
        elif isinstance(other, (MultielementPolynomial, Number, Variable)):
            return MultielementPolynomial(self) + other
        else:
            raise ValueError()

    def __sub__(self, other):
        if isinstance(other, Item):
            # 判断是否能合并
            if (self.sub_item == other.sub_item):
                coefficient_result = self.coefficient - other.coefficient
                return Item(coefficient_result, self.sub_item)
            return MultielementPolynomial(self, -other)
        elif isinstance(other, (MultielementPolynomial, Number, Variable)):
            return MultielementPolynomial(self) - other
        else:
            raise ValueError()

    def __mul__(self, other):
        if isinstance(other, Item):
            return Item(self.coefficient * other.coefficient, self.sub_item * other.sub_item)
        elif isinstance(other, MultielementPolynomial):
            return MultielementPolynomial(self) * other
        elif isinstance(other, Number):
            return Item(self.coefficient * other.value, self.sub_item)
        elif isinstance(other, Variable):
            return Item(self.coefficient, self.sub_item * other)
        else:
            raise ValueError()

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            return Item(self.coefficient ** power.value, self.sub_item ** power)
        elif isinstance(power, Item) and power.sub_item.is_empty:
            return Item(self.coefficient ** power.coefficient, self.sub_item ** power.coefficient)
        else:
            raise NotImplementedError("暂不支持幂为其他类型的情况")


class SubItem(Node):
    def __init__(self, **kwargs):
        self.var_pow_dict = kwargs

    @property
    def is_empty(self):
        return not bool(self.var_pow_dict)

    def __str__(self):
        buffer = []
        for c, e in self.var_pow_dict.items():
            if e == 1:
                buffer.append(f"{c}")
            else:
                buffer.append(f"{c}^{e}")
        return "*".join(buffer)

    def __eq__(self, other):
        if isinstance(other, SubItem):
            return self.var_pow_dict == other.var_pow_dict

    def __getitem__(self, item):
        return self.var_pow_dict.get(item, 0)

    def __mul__(self, other):
        if isinstance(other, SubItem):
            new_var_pow_dict = self.var_pow_dict.copy()

            for k, v in other.var_pow_dict.items():
                if k in new_var_pow_dict:
                    new_var_pow_dict[k] += v
                else:
                    new_var_pow_dict[k] = v

        elif isinstance(other, Variable):
            new_var_pow_dict = self.var_pow_dict.copy()

            if other.value in new_var_pow_dict:
                new_var_pow_dict[other.value] += 1
            else:
                new_var_pow_dict[other.value] = 1
        else:
            raise ValueError()

        return SubItem(**new_var_pow_dict)

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            return SubItem(**{k: v * power.value for k, v in self.var_pow_dict.items()})
        elif isinstance(power, (int, float)):
            return SubItem(**{k: v * power for k, v in self.var_pow_dict.items()})
        else:
            raise NotImplementedError("暂不支持幂为其他类型的情况")

    def append(self, var, pow=1):
        if pow == 0:
            return
        self.var_pow_dict[var] = pow


def pre_traverse(root, callback=None):
    '''
    前序遍历
    '''
    if root is None:
        return
    callback and callback(root)
    pre_traverse(getattr(root, "l_value", None), callback)
    pre_traverse(getattr(root, "r_value", None), callback)


def mid_traverse(root, callback=None):
    '''
    中序遍历
    '''
    if root is None:
        return
    mid_traverse(getattr(root, "l_value", None), callback)
    callback and callback(root)
    mid_traverse(getattr(root, "r_value", None), callback)


def after_traverse(root, callback=None):
    '''
    后序遍历
    '''
    if root is None:
        return
    after_traverse(getattr(root, "l_value", None), callback)
    after_traverse(getattr(root, "r_value", None), callback)
    callback and callback(root)
