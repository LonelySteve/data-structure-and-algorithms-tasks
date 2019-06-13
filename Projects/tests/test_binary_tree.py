from binary_tree import BinaryTree, HuffmanTree


class TestBinaryTree(object):
    def get_example_tree_0(self):
        th = BinaryTree.VOID_NODE_PLACEHOLDER
        t = BinaryTree.create(f"123{th}{th}4{th}{th}5{th}{th}")
        return t

    def get_example_tree_1(self):
        t = BinaryTree.create("")
        return t

    def get_example_tree_2(self):
        # 这本来是个错误的例子
        t = BinaryTree.create("1")
        return t

    def test_create(self):
        t = self.get_example_tree_0()
        t.root.value = "1"
        t.root.left_node.value = "2"
        t.root.right_node.value = "5"
        t.root.left_node.left_node.value = "3"
        t.root.left_node.right_node.value = "4"
        t = self.get_example_tree_1()
        assert t.root == None
        t = self.get_example_tree_2()
        assert t.root.value == "1"

    def test_depth(self):
        t = self.get_example_tree_0()
        assert t.depth == 3
        t = self.get_example_tree_1()
        assert t.depth == 0
        t = self.get_example_tree_2()
        assert t.depth == 1

    def test_is_exist(self):
        t = self.get_example_tree_0()
        assert not t.is_exist(lambda node: node.value == "0")
        assert t.is_exist(lambda node: node.value == "1")
        assert t.is_exist(lambda node: node.value == "2")
        assert t.is_exist(lambda node: node.value == "3")
        assert t.is_exist(lambda node: node.value == "4")
        assert t.is_exist(lambda node: node.value == "5")
        t = self.get_example_tree_1()
        assert not t.is_exist(lambda node: node.value == "0")
        t = self.get_example_tree_2()
        assert not t.is_exist(lambda node: node.value == "0")
        assert t.is_exist(lambda node: node.value == "1")

    def test_pre_order_traverse(self):
        values = []
        t = self.get_example_tree_0()
        t.pre_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == "12345"
        values = []
        t = self.get_example_tree_1()
        t.pre_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == ""
        values = []
        t = self.get_example_tree_2()
        t.pre_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == "1"

    def test_in_order_traverse(self):
        values = []
        t = self.get_example_tree_0()
        t.in_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == "32415"
        values = []
        t = self.get_example_tree_1()
        t.in_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == ""
        values = []
        t = self.get_example_tree_2()
        t.in_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == "1"

    def test_post_order_traverse(self):
        values = []
        t = self.get_example_tree_0()
        t.post_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == "34251"
        values = []
        t = self.get_example_tree_1()
        t.post_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == ""
        values = []
        t = self.get_example_tree_2()
        t.post_order_traverse(lambda node: values.append(node.value))
        assert "".join(values) == "1"

    def test_end_node_count(self):
        t = self.get_example_tree_0()
        assert t.end_node_count == 3
        t = self.get_example_tree_1()
        assert t.end_node_count == 0
        t = self.get_example_tree_2()
        assert t.end_node_count == 1

    def test_get_node_parent(self):
        t = self.get_example_tree_0()
        assert t.get_node_parent(lambda node: node.value == "2").value == "1"
        assert t.get_node_parent(lambda node: node.value == "1") is None
        assert t.get_node_parent(lambda node: node.value == "3").value == "2"
        assert t.get_node_parent(lambda node: node.value == "5").value == "1"
        t = self.get_example_tree_1()
        assert t.end_node_count == 0
        assert t.get_node_parent(lambda node: node.value == "2") is None
        t = self.get_example_tree_2()
        assert t.end_node_count == 1
        assert t.get_node_parent(lambda node: node.value == "1") is None

    def test_get_node_sibling(self):
        t = self.get_example_tree_0()
        assert t.get_node_sibling(lambda node: node.value == "0") is None
        assert t.get_node_sibling(lambda node: node.value == "2").value == "5"
        assert t.get_node_sibling(lambda node: node.value == "4").value == "3"
        assert t.get_node_sibling(lambda node: node.value == "1") is None
        assert t.get_node_sibling(lambda node: node.value == "5").value == "2"
        t = self.get_example_tree_1()
        assert t.get_node_sibling(lambda node: node.value == "5") is None
        t = self.get_example_tree_2()
        assert t.get_node_sibling(lambda node: node.value == "1") is None


class TestHuffmanTree(object):
    def get_example_tree_0(self):
        def_dict = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
        }
        return HuffmanTree.create(def_dict)

    def get_example_tree_1(self):
        def_dict = {
            "E": 1,
            "D": 2,
            "C": 3,
            "B": 4,
            "A": 5,
        }
        return HuffmanTree.create(def_dict)

    def get_example_tree_2(self):
        def_dict = {}
        return HuffmanTree.create(def_dict)

    def test_create(self):
        t = self.get_example_tree_0()
        assert t.root.value == 15
        assert t.root.left_node.value == 6
        assert t.root.right_node.value == 9
        self.get_example_tree_1()
        self.get_example_tree_2()

    def test_dump_code_dict(self):
        t = self.get_example_tree_0()
        assert t.dump_code_dict() == {
            "A": [0, 1, 0],
            "B": [0, 1, 1],
            "C": [0, 0],
            "D": [1, 0],
            "E": [1, 1]
        }
