from typing import Optional
from enum import Enum, unique


@unique
class BinaryTreeChildSelect(Enum):
    left = 0,
    right = 1


class BinaryTreeNode(object):
    """
    树结点 继承于 树
    """

    def __init__(self, left_node=None, right_node=None, value=None):
        super().__init__()
        self.left_node = left_node
        self.right_node = right_node
        self.value = value

    def __repr__(self):
        return f"<BinaryTreeNode value='{self.value}'>"

    @property
    def depth(self):
        if self.left_node is None:
            left_child_depth = 0
        else:
            left_child_depth = self.left_node.depth
        if self.right_node is None:
            right_child_depth = 0
        else:
            right_child_depth = self.right_node.depth

        return max(left_child_depth, right_child_depth) + 1

    def insert_child(self, select: BinaryTreeChildSelect, node):
        # 检查结点的右子树为空
        if node.right_node is not None:
            raise ValueError("插入结点的右结点不为空！")
        if select == BinaryTreeChildSelect.left:
            src_node = self.left_node
        elif select == BinaryTreeChildSelect.right:
            src_node = self.right_node
        else:
            raise TypeError
        # 插入的结点的右孩子被设置为原插入位置的结点
        node.right_node = src_node
        self.left_node = node

    def pre_order_traverse(self, visit_callback):
        """
        使用指定的遍历回调函数前序遍历当前结点

        :param visit_callback:
        :return:
        """
        result = visit_callback(self)
        if result:
            return result
        if self.left_node is not None:
            result = self.left_node.pre_order_traverse(visit_callback)
            if result:
                return result
        if self.right_node is not None:
            result = self.right_node.pre_order_traverse(visit_callback)
            if result:
                return result

    def in_order_traverse(self, visit_callback):
        """
        使用指定的遍历回调函数中序遍历当前结点

        :param visit_callback:
        :return:
        """
        if self.left_node is not None:
            result = self.left_node.in_order_traverse(visit_callback)
            if result:
                return result
        result = visit_callback(self)
        if result:
            return result
        if self.right_node is not None:
            result = self.right_node.in_order_traverse(visit_callback)
            if result:
                return result

    def post_order_traverse(self, visit_callback):
        """
        使用指定的遍历回调函数后序遍历当前结点

        :param visit_callback:
        :return:
        """
        if self.left_node is not None:
            result = self.left_node.post_order_traverse(visit_callback)
            if result:
                return result
        if self.right_node is not None:
            result = self.right_node.post_order_traverse(visit_callback)
            if result:
                return result
        result = visit_callback(self)
        if result:
            return result

    @property
    def end_node_count(self):
        if self.left_node is None:
            left_child_end_node = 0
        else:
            left_child_end_node = self.left_node.end_node_count

        if self.right_node is None:
            right_child_end_node = 0
        else:
            right_child_end_node = self.right_node.end_node_count

        # 如果左右结点没有任何一个具有终端结点，则返回1（即当前结点为终端结点），否则返回左右结点终端结点数之和
        if not any([left_child_end_node, right_child_end_node]):
            return 1
        else:
            return left_child_end_node + right_child_end_node


class BinaryTree:
    """
    二叉树
    """

    def __init__(self, root):
        """实例化新的树实例"""
        self.root = root

    @staticmethod
    def create(definition):
        """根据前序字符串二叉树定义创建二叉树"""

        char_list = list(definition)

        def recursion():

            if not char_list:
                return None

            ch = char_list.pop(0)

            if ch == '$':
                return None
            else:
                new_node = BinaryTreeNode()
                new_node.left_node = recursion()
                new_node.right_node = recursion()
                new_node.value = ch
                return new_node

        return BinaryTree(recursion())

    @property
    def is_empty(self):
        """判断当前树是否为空树"""
        return self.root is None

    @property
    def depth(self):
        """获取当前树的深度"""
        if self.root is None:
            return 0

        return self.root.depth

    @property
    def end_node_count(self):
        """
        获取当前树的终端结点总数

        :return:
        """
        if self.root is None:
            return 0
        return self.root.end_node_count

    def get_node_parent(self, node_select_callback):
        """
        使用先序遍历获取选择回调函数指定结点的父结点
        :return:
        """
        if self.root is None:
            return None

        def traverse_callback(node):
            if (node.left_node and node_select_callback(node.left_node)) or \
                    (node.right_node and node_select_callback(node.right_node)):
                return node

        return self.root.pre_order_traverse(traverse_callback)

    def get_node_sibling(self, node_select_callback):
        """
        使用先序遍历获取选择回调函数指定结点的兄弟结点
        :return:
        """
        if self.root is None:
            return None

        def traverse_callback(node):
            # 当前结点左结点存在且符合选择回调函数，返回当前结点的右结点
            if node.left_node and node_select_callback(node.left_node):
                return node.right_node
            # 当前结点右结点存在且符合选择回调函数，返回当前结点的左结点
            if node.right_node and node_select_callback(node.right_node):
                return node.left_node

        return self.root.pre_order_traverse(traverse_callback)

    def clear(self):
        """清空树"""
        self.root = None

    def is_exist(self, node_select_callback) -> bool:
        """
        判断当前树中是否存在符合指定结点选择回调函数的结点

        :param node: 欲查询的指定结点
        :return: 存在返回 True，否则返回 False
        """
        if self.root is None:
            return False

        def exist_callback(node):
            if node_select_callback(node):
                return True

        return bool(self.root.pre_order_traverse(exist_callback))

    def pre_order_traverse(self, visit_callback):
        """
        使用指定访问回调函数对当前树的结点进行先序遍历访问

        :param visit_callback: 访问器
        :return: None
        """
        if self.root is not None:
            self.root.pre_order_traverse(visit_callback)

    def in_order_traverse(self, visit_callback):
        """
        使用指定访问回调函数对当前树的结点进行中序遍历访问

        :param visit_callback:
        :return:
        """
        if self.root is not None:
            self.root.in_order_traverse(visit_callback)

    def post_order_traverse(self, visit_callback):
        """
        使用指定访问回调函数对当前树的结点进行后序遍历访问

        :param visit_callback:
        :return:
        """
        if self.root is not None:
            self.root.post_order_traverse(visit_callback)
