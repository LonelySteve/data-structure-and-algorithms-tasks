from itertools import groupby

from MultielementPolynomial.src.mpnode import MPNode


class MPList(object):
    def  __init__(self, var):
        self.head = None
        self.tail = None
        self.var = var

    def __getitem__(self, item):
        result = self.get_mplist_list(item)
        if not result:
            l = MPList(item)
            result = [l]
        return iter(result)

    def get_mplist_list(self, var):
        ret_val = []

        if self.var == var:
            ret_val.append(self)
            return ret_val

        cur_node = self.head

        while cur_node is not None:
            if cur_node.mplist is None:
                cur_node = cur_node.next
                continue
            if cur_node.mplist.var == var:
                ret_val.append(cur_node.mplist)
            else:
                flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
                result = cur_node.mplist.get_mplist_list(var)
                ret_val += flatten(result)

            cur_node = cur_node.next

        return ret_val

    def __iter__(self):
        cur_node = self.head
        while cur_node is not None:
            yield cur_node
            cur_node = cur_node.next

    def append(self, node):
        if self.tail == None:
            self.tail = node
            self.head = node
            node.next = None
        else:
            self.tail.next = node
            node.next = None
            self.tail = node

    def __mul__(self, other):
        if isinstance(other, MPList):
            big_list, small_list = self, other
            if self.var < other.var:
                big_list, small_list = small_list, big_list

            retList = MPList(big_list.var)

            for node_1 in big_list:
                for list in small_list[big_list.var]:
                    for node_2 in list:
                        node = node_1 * node_2
                        retList.append(node)

            return retList
        elif isinstance(other,(int,float)):
            retList = MPList(self.var)
            for item in self:
                retList.append(item * other)
        else:
            raise ValueError("不支持与MPList之外的表达式相乘")

    def __repr__(self):
        return f"{self.var}({', '.join([str(node) for node in self])})"


def get_mp_struct(items, vars):
    retval = {}

    if not vars:
        return next(iter(items)).coefficient

    var = vars.pop()

    # 根据当前变元的指数值分组
    result = groupby(items, lambda item: item.sub_item[var])
    for k, items in result:
        vars_copy = list(vars)
        retval[k] = get_mp_struct([item for item in items], vars_copy)
    return retval


def convert(mp):
    """从多元多项式转换到多元多项式广义表"""
    vars = list(mp.vars)
    vars.sort()

    mp_struct = get_mp_struct(mp.get_value(), vars)

    def deep(d, vars):
        if not vars:
            return d

        var = vars.pop()

        mp_list = MPList(var)

        for exp, value in d.items():
            vars_copy = list(vars)
            v = deep(value, vars_copy)
            if isinstance(v, MPList):
                mp_list.append(MPNode(exp, mplist=v))
            else:
                mp_list.append(MPNode(exp, value))
        return mp_list

    vars = list(mp.vars)
    vars.sort()

    return deep(mp_struct, vars)
