import os
import time
from binary_tree import BinaryTree, HuffmanTree
from graph import DirectedGraph, UndirectedGraph, DirectedNetwork, UndirectedNetwork


def flash_message(message, keep_time=3):
    i = os.system("cls")
    print(message)
    time.sleep(keep_time)


def option_catcher(option_handle_callback):
    i = input("请选择：")
    no = int(i)
    try:
        return option_handle_callback(no)
    except KeyError:
        flash_message(f"不存在的选项 {no} 请重新选择！")
    except ValueError:
        flash_message(f"无法转换为数字的字符串：{i}")
    except Exception as ex:
        flash_message(str(ex))


class BinaryTreeController(object):
    """二叉树控制器"""

    def __init__(self):
        self.binary_tree = None  # type: BinaryTree

    def _raise_if_not_binary_tree(self):
        if self.binary_tree is None:
            raise Exception("请先构建二叉树！")

    def create(self):
        os.system("cls")
        code = input(f"请输入前序遍历表示的二叉树（可使用'{BinaryTree.VOID_NODE_PLACEHOLDER}'表示空节点）：")
        self.binary_tree = BinaryTree.create(code)
        flash_message("构建完成...")

    def traverse(self):
        if self.binary_tree is None:
            raise Exception("请先构建二叉树！")

        def visit_callback(node):
            print(node.value, end="")

        def pre_order_traverse():
            self.binary_tree.pre_order_traverse(visit_callback)

        def in_order_traverse():
            self.binary_tree.in_order_traverse(visit_callback)

        def post_order_traverse():
            self.binary_tree.post_order_traverse(visit_callback)

        options = {
            1: pre_order_traverse,
            2: in_order_traverse,
            3: post_order_traverse,
            5: quit
        }

        while True:
            print("***********二叉树遍历***********")
            print("* 1  前序遍历                  *")
            print("* 2  中序遍历                  *")
            print("* 3  后序遍历                  *")
            print("* 4  返回上一层                *")
            print("* 5  退出                     *")
            print("*******************************")

            try:
                if option_catcher(lambda no: True if no == 4 else options[no]()):
                    break
            except Exception:
                pass

    def cal_depth(self):
        self._raise_if_not_binary_tree()
        flash_message(f"该树的深度为：{self.binary_tree.depth}")

    def cal_end_node_count(self):
        self._raise_if_not_binary_tree()
        flash_message(f"该树的终端节点数为：{self.binary_tree.end_node_count}")

    def find_parent(self):
        self._raise_if_not_binary_tree()
        name = input("请输入欲查找双亲的结点名：")
        result = self.binary_tree.get_node_parent(lambda node: node.value == name)
        if result:
            flash_message(f"{name}的双亲是{result.value}")
        else:
            flash_message(f"未能找到{name}的双亲")

    def find_sibling(self):
        self._raise_if_not_binary_tree()
        name = input("请输入欲查找兄弟的结点名：")
        result = self.binary_tree.get_node_sibling(lambda node: node.value == name)
        if result:
            flash_message(f"{name}的兄弟是{result.value}")
        else:
            flash_message(f"未能找到{name}的兄弟")

    def huffman_coding(self):
        not_encoding_chars = list(input("请输入一段待编码的字符串："))
        with_weight_chars = {}
        for char in set(not_encoding_chars):
            while True:
                try:
                    weight = int(input(f"请输入{char}的权重："))
                    with_weight_chars.update({char: weight})
                    break
                except ValueError:
                    print("请输入正确的值！")

        t = HuffmanTree.create(with_weight_chars)
        code_dict = t.dump_code_dict()
        temp_stack = []
        for char_encoding_info in sorted(code_dict.items(), key=lambda k: not_encoding_chars.index(k[0])):
            encoding = ''.join([str(s) for s in char_encoding_info[1]])
            temp_stack.append(encoding)
            print(f"{char_encoding_info[0]}的编码是{encoding}")

        print()  # 空行
        flash_message(f"该字符串的哈夫曼编码为：{' '.join(temp_stack)}")


class GraphController(object):
    """图控制器"""

    def __init__(self):
        self.graphs = {}

    def _name_maker(self, prefix="未命名"):
        index = 1
        while True:
            new_name = f"{prefix}_{index}"
            if new_name not in [name for name, graph in self.graphs.items()]:
                return new_name
            index += 1

    def _create_graph(self, cls, cls_name, has_order=True, with_weight=True):
        name_ok = False
        name = None
        while not name_ok:
            name = input(f"请输入{cls_name}的名称（可留空）：")
            if name:
                if name in (id_ for id_, graph in self.graphs.items()):
                    while True:
                        result = input("名称已存在，是否覆盖原图？(Y/n)")
                        if result.lower() == "y":
                            self.graphs[name] = cls()
                            name_ok = True
                            break
                        elif result.lower() == "n":
                            break
                else:
                    self.graphs[name] = cls()
                    name_ok = True
            else:
                name = self._name_maker(cls_name)
                self.graphs[name] = cls()
                name_ok = True

        g = self.graphs[name]

        vertex_names = input("请输入顶点名称（使用空白符分隔）：\n").split()
        g.extend_vertexes(*vertex_names)

        while True:
            try:
                edge_count = int(input("请输入边的数量："))
                break
            except ValueError:
                print("请输入正确的值！")

        print("=================输入边信息=====================")
        tips = []
        if has_order:
            tips.append("两个顶点从左到右为代表该边的指向")
        else:
            tips.append("两个顶点不分顺序")
        if with_weight:
            tips.append("使用空白符间隔三个参数，从左到右为 <顶点名称1> <顶点名称2> <边权值>")
        else:
            tips.append("使用空白符间隔两个参数，从左到右为 <顶点名称1> <顶点名称2>")
        # 打印提示
        for i, tip in enumerate(tips):
            print(f"{i} . {tip}")
        print()  # 换行
        for i in range(edge_count):
            while True:
                try:
                    if with_weight:
                        v1, v2, w = input(f"请输入第{i + 1}条边信息：").split()
                        g.add_new_edge(v1, v2, int(w))
                    else:
                        v1, v2 = input(f"请输入第{i + 1}条边信息：").split()
                        g.add_new_edge(v1, v2)
                    break
                except Exception as ex:
                    print("错误：" + str(ex))
        print("================================================")
        print(f"创建的新{cls_name}的名称为：{name}")
        print(f"该{cls_name}的邻接矩阵为：")
        self._print_adjacency_matrix(g)
        flash_message("创建完成...")

    def _print_adjacency_matrix(self, g):
        # 首先遍历邻接矩阵每一个元素，取最大值
        max_elem = 0
        for row in g.adjacency_matrix:
            for elem in row:
                if elem > max_elem:
                    max_elem = elem

        max_elem_len = len(str(max_elem))
        # 打印邻接矩阵
        for row in g.adjacency_matrix:
            for elem in row:
                if elem <= g.DEFAULT_UNREACHABLE_MAX_VALUE:
                    # 对于网应当打印出无限符号
                    if isinstance(g, (UndirectedNetwork, DirectedNetwork)):
                        print(f"{'∞':>{max_elem_len + 1}}", end='')  # 右对齐，宽度为最大元素的字面值长度加1
                    else:
                        print(f"{g.DEFAULT_UNREACHABLE_MAX_VALUE:>{max_elem_len + 1}}", end='')  # 右对齐，宽度为最大元素的字面值长度加1

                else:
                    print(f"{elem:>{max_elem_len + 1}}", end='')  # 右对齐，宽度为最大元素的字面值长度加1
            print()  # 换行

    def _select_graph(self, cls_s, cls_names):
        available_graphs = [g_ for g_ in self.graphs.items() if isinstance(g_[1], cls_s)]
        if not available_graphs:
            raise RuntimeError(f"请先创建{', '.join(cls_names)}的实例后再操作！")

        print(f"从下列{', '.join(cls_names)}的实例中选择一个：")
        g_list = []
        for i, g in enumerate(available_graphs):
            g_list.append(g[1])
            print(f"{i}.{g[0]}")
        print()  # 空行

        def handler(no):
            if not (0 <= no < len(self.graphs)):
                raise KeyError

            return no

        while True:
            selected_graph_no = option_catcher(handler)
            if selected_graph_no is not None:
                break

        return g_list[selected_graph_no]

    def create_undirected_graph(self):
        self._create_graph(UndirectedGraph, "无向图", False, False)

    def create_directed_graph(self):
        self._create_graph(DirectedGraph, "有向图", True, False)

    def create_undirected_network(self):
        self._create_graph(UndirectedNetwork, "无向网", False, True)

    def create_directed_network(self):
        self._create_graph(DirectedNetwork, "有向网", True, True)

    def traverse(self):
        g = self._select_graph((UndirectedGraph, DirectedGraph, DirectedNetwork, UndirectedNetwork),
                               ("无向图", "有向图", "有向网", "无向网"))

        def visit_callback(vertex):
            print(vertex.name, end="")

        start_vertex_name = input("请输入遍历起始点的名称：")

        print("BFS 遍历结果：", end="")
        g.bfs_traverse(start_vertex_name, visit_callback)
        print()
        print("DFS 遍历结果：", end="")
        g.dfs_traverse(start_vertex_name, visit_callback)
        flash_message('')

    def topological_sort(self):
        g = self._select_graph((DirectedGraph, DirectedNetwork), ("有向图", "有向网"))

        flash_message(f"拓扑排序结果：{''.join([v.name for v in g.topological_sort()])}")

    def get_minimum_spanning_tree(self):
        g = self._select_graph((DirectedNetwork, UndirectedNetwork), ("有向网", "无向网"))

        tree = g.get_minimum_spanning_tree()

        print("该最小生成树的邻接表：")
        for v, adj_vs in tree.adjacency_dict.items():
            print(f"{v.name}: {','.join([v.name for v in adj_vs])}")
        print("该最小生成树的邻接矩阵：")
        self._print_adjacency_matrix(tree)

    def find_shortest_paths(self):
        g = self._select_graph((UndirectedGraph, DirectedGraph, DirectedNetwork, UndirectedNetwork),
                               ("无向图", "有向图", "有向网", "无向网"))
        start_vertex_name = input("请输入起始点的名称：")
        end_vertex_name = input("请输入终点的名称：")
        # 判断 g 的类型，对于最短路径，带边权与不带边权的算法不一样
        if isinstance(g, (UndirectedGraph, DirectedGraph)):
            shortest_path = g.find_shortest_path(start_vertex_name, end_vertex_name)
            flash_message(f"最短路径为 {'->'.join([v.name for v in shortest_path])}")
        else:
            shortest_paths = g.find_shortest_paths_with_weight(start_vertex_name, end_vertex_name)
            flash_message(f"最短路径为 {'->'.join([v.name for v in shortest_paths[0][0]])}")

    def find_critical_paths(self):
        g = self._select_graph((DirectedNetwork, UndirectedNetwork), ("有向网"))
        paths = g.find_critical_paths()
        print("关键路径有：")
        for path in paths:
            print(f"{'->'.join([v.name for v in path])}")


def binary_tree():
    t = BinaryTreeController()
    options = {
        1: t.create,
        2: t.traverse,
        3: t.cal_depth,
        4: t.cal_end_node_count,
        5: t.find_parent,
        6: t.find_sibling,
        7: t.huffman_coding,
        9: quit
    }
    while True:
        print("**************二叉树的基本操作及应用***************")
        print("* 1  创建二叉树                                 *")
        print("* 2  遍历二叉树（先/中/后）                       *")
        print("* 3  计算树的深度                                *")
        print("* 4  计算叶子结点个数                             *")
        print("* 5  查找双亲                                    *")
        print("* 6  查找兄弟                                    *")
        print("* 7  Huffman编码（应用）                          *")
        print("* 8  返回上一层                                   *")
        print("* 9  退出                                        *")
        print("***************************************************")

        if option_catcher(lambda no: True if no == 8 else options[no]()):
            break


def graph():
    g = GraphController()
    options = {
        1: g.create_undirected_graph,
        2: g.create_undirected_network,
        3: g.create_directed_graph,
        4: g.create_directed_network,
        5: g.traverse,
        6: g.topological_sort,
        7: g.get_minimum_spanning_tree,
        8: g.find_shortest_paths,
        9: g.find_critical_paths,
        11: quit
    }
    while True:
        print("****************图的基本操作及应用*****************")
        print("* 1  创建无向图                                  *")
        print("* 2  创建无向网                                  *")
        print("* 3  创建有向图                                  *")
        print("* 4  创建有向网                                  *")
        print("* 5  遍历                                       *")
        print("* 6  拓扑排序                                    *")
        print("* 7  最小生成树（应用）                            *")
        print("* 8  最短路径（应用）                              *")
        print("* 9  关键路径（应用）                              *")
        print("* 10 返回上一层                                   *")
        print("* 11 退出                                        *")
        print("***************************************************")

        if option_catcher(lambda no: True if no == 10 else options[no]()):
            break


def quit():
    flash_message("再见！")
    exit(0)


def main():
    options = {
        1: binary_tree,
        2: graph,
        3: quit
    }
    while True:
        print("*******************算法与数据结构******************")
        print("* 1  树的基本操作及应用                            *")
        print("* 2  图的基本操作及应用                            *")
        print("* 3  退出                                        *")
        print("*************************************************")

        option_catcher(lambda no: options[no]())


if __name__ == '__main__':
    main()
