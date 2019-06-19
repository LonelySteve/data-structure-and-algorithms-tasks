import exceptions


class Vertex(object):
    """顶点"""

    def __init__(self, name, value=None):
        """
        初始化新实例 Vertex

        :param name: 顶点名称，不同网络可以拥有相同名称的顶点
        :param value: 顶点值，默认为None
        """
        # 名称应该可以被正确取得hash值
        hash(name)
        self.name = name
        self.value = value

    def __hash__(self):
        """获取哈希值"""
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.name == other.name and self.value == other.value
        return False

    def __repr__(self):
        return f"<Vertex '{self.name}'={self.value}>"


class Edge(object):
    def __init__(self, weight=None):
        self.weight = weight
        self.iter_counter = -1

    def __lt__(self, other):
        return self.weight < other.weight

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError

    def reset(self):
        self.iter_counter = -1

    def has_vertex(self, vertex):
        return NotImplementedError

    def other_vertex(self, vertex):
        return NotImplementedError


class DirectedEdge(Edge):
    """有向边"""

    def __init__(self, from_vertex, to_vertex, weight=None):
        super().__init__(weight)
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex

    def __repr__(self):
        return f"({self.from_vertex}->{self.to_vertex})"

    def __next__(self):
        if self.iter_counter >= 2:
            raise StopIteration
        self.iter_counter += 1
        return self.from_vertex if self.iter_counter == 0 else self.to_vertex

    def __eq__(self, other):
        if isinstance(other, DirectedEdge):
            return self.from_vertex == other.to_vertex and self.to_vertex == other.to_vertex
        return False

    def has_vertex(self, vertex):
        return vertex == self.from_vertex or vertex == self.to_vertex

    def other_vertex(self, vertex):
        if vertex == self.from_vertex:
            return self.to_vertex
        elif vertex == self.to_vertex:
            return self.from_vertex


class UndirectedEdge(Edge):
    """无向边"""

    def __init__(self, vertex_a, vertex_b, weight=None):
        super().__init__(weight)
        self.vertex_pair = {vertex_a, vertex_b}
        self.weight = weight

    def __repr__(self):
        vertex_pair = list(self.vertex_pair)
        return f"({vertex_pair[0]}-{vertex_pair[1]})"

    def __next__(self):
        if self.iter_counter >= 2:
            raise StopIteration
        self.iter_counter += 1
        vertex_pair = list(self.vertex_pair)
        return vertex_pair[self.iter_counter]

    def __eq__(self, other):
        if isinstance(other, UndirectedEdge):
            return self.vertex_pair == other.vertex_pair
        return False

    def has_vertex(self, vertex):
        return vertex in self.vertex_pair

    def other_vertex(self, vertex):
        if vertex in self.vertex_pair:
            vs = list(self.vertex_pair)
            return vs[1] if vertex == vs[0] else vs[0]


class Graph(object):
    """图"""
    EDGE_CLS = None
    # 默认表示可达的邻接矩阵元素值
    DEFAULT_REACHABLE_VALUE = 1
    # 默认表示不可达的邻接矩阵最大元素值
    DEFAULT_UNREACHABLE_MAX_VALUE = 0

    def __init__(self, *vertexes):
        self.vertexes = []
        self.edges = []
        vertexes = vertexes or []
        self.extend_vertexes(*vertexes)
        if self.EDGE_CLS is None:
            raise NotImplementedError

    def get_vertex_by_name(self, vertex_name):
        try:
            return next(v for v in self.vertexes if v.name == vertex_name)
        except StopIteration:
            raise exceptions.VertexNotExistError(f"名称为'{vertex_name}'的顶点不存在！")

    def add_new_edge(self, from_vertex_name, to_vertex_name, weight=None):
        from_vertex = self.get_vertex_by_name(from_vertex_name)
        to_vertex = self.get_vertex_by_name(to_vertex_name)
        # 具体使用何种边类由具体的实现类决定
        new_edge = self.EDGE_CLS(from_vertex, to_vertex, weight)

        if new_edge not in self.edges:
            self.edges.append(new_edge)

    def add_edge(self, edge):
        if self.EDGE_CLS == UndirectedEdge and not isinstance(edge, UndirectedEdge):
            raise exceptions.EdgeTypeError
        elif self.EDGE_CLS == DirectedEdge and not isinstance(edge, DirectedEdge):
            raise exceptions.EdgeTypeError

        self.edges.append(edge)

    def extend_edges(self, *edges):
        for edge in edges:
            self.add_edge(edge)

    def add_vertex(self, vertex):
        if isinstance(vertex, str):
            vertex = Vertex(vertex)
        elif not isinstance(vertex, Vertex):
            raise exceptions.VertexTypeError

        if vertex not in self.vertexes:
            self.vertexes.append(vertex)

    def extend_vertexes(self, *vertexes):
        for v in vertexes:
            self.add_vertex(v)

    @property
    def adjacency_matrix(self):
        """获取邻接矩阵"""
        # 初始化邻接矩阵，填充不可达的值
        temp_adjacency_matrix = [[self.DEFAULT_UNREACHABLE_MAX_VALUE for _ in range(len(self.vertexes))] for _ in
                                 range(len(self.vertexes))]

        adjacency_dict = self.adjacency_dict
        for i, vertex in enumerate(self.vertexes):
            for adj_vertex in adjacency_dict[vertex]:
                j = self.vertexes.index(adj_vertex)
                temp_adjacency_matrix[i][j] = self.DEFAULT_REACHABLE_VALUE
                try:
                    # 如果找到了两个顶点的边，且边有权值，则重新赋值为该权值
                    edge = self.find_edge(vertex, adj_vertex)
                    if edge.weight is not None:
                        temp_adjacency_matrix[i][j] = edge.weight
                except StopIteration:
                    pass

        return temp_adjacency_matrix

    @property
    def adjacency_dict(self):
        """获取邻接字典"""
        # 初始化邻接字典
        temp_adj_dict = {v: [] for v in self.vertexes}

        for v, row in temp_adj_dict.items():
            if self.EDGE_CLS == DirectedEdge:
                for edge in (e for e in self.edges if e.from_vertex == v):
                    row.append(edge.to_vertex)
            elif self.EDGE_CLS == UndirectedEdge:
                for edge in (e for e in self.edges if e.has_vertex(v)):
                    row.append(edge.other_vertex(v))

        return temp_adj_dict

    @property
    def reversed_adjacency_dict(self):
        """逆邻接字典"""
        temp_adj_dict = {v: [] for v in self.vertexes}

        for v, row in temp_adj_dict.items():
            if self.EDGE_CLS == DirectedEdge:
                for edge in (e for e in self.edges if e.to_vertex == v):
                    row.append(edge.from_vertex)
            elif self.EDGE_CLS == UndirectedEdge:
                for edge in (e for e in self.edges if e.has_vertex(v)):
                    row.append(edge.other_vertex(v))

        return temp_adj_dict

    def bfs_traverse(self, start_vertex_name, visit_callback):
        adj_dict = self.adjacency_dict
        start_vertex = self.get_vertex_by_name(start_vertex_name)

        def bfs():
            visited, queue = set(), [start_vertex]
            while queue:
                vertex = queue.pop(0)
                if vertex not in visited:
                    flag = visit_callback(vertex)
                    if flag:
                        return flag
                    visited.add(vertex)
                    for next_vertex in adj_dict[vertex]:
                        if next_vertex not in visited:
                            queue.append(next_vertex)
            return visited

        bfs()

    def dfs_traverse(self, start_vertex_name, visit_callback):
        adj_dict = self.adjacency_dict
        start_vertex = self.get_vertex_by_name(start_vertex_name)

        def dfs():
            visited, stack = set(), [start_vertex]
            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    flag = visit_callback(vertex)
                    if flag:
                        return flag
                    visited.add(vertex)
                    for next_vertex in adj_dict[vertex]:
                        if next_vertex not in visited:
                            stack.append(next_vertex)
            return visited

        dfs()

    def get_minimum_spanning_tree(self):

        edges = [edge for edge in self.edges if edge.weight]  # 去除无权边
        # 按照权重从小到大将边进行排序
        sorted_edges = list(sorted(edges, key=lambda edge: edge.weight))

        CLS = DirectedNetwork if self.EDGE_CLS == DirectedEdge else UndirectedNetwork

        graphs = [CLS(v) for v in self.vertexes]
        # 排序至只有一个图时结束
        while len(graphs) != 1:
            try:
                edge = sorted_edges.pop(0)
            except IndexError:
                raise RuntimeError("该图/网非连通！")
            v_a = next(edge)
            v_b = next(edge)
            has_v_a_graph = next(graph for graph in graphs if v_a in graph.vertexes)
            has_v_b_graph = next(graph for graph in graphs if v_b in graph.vertexes)
            if has_v_a_graph is not has_v_b_graph:
                new_graph = CLS()
                new_graph.extend_vertexes(*(has_v_a_graph.vertexes + has_v_b_graph.vertexes))
                new_graph.extend_edges(*(has_v_a_graph.edges + has_v_b_graph.edges))
                new_graph.add_new_edge(v_a.name, v_b.name)
                graphs.pop(graphs.index(has_v_a_graph))
                graphs.pop(graphs.index(has_v_b_graph))
                graphs.append(new_graph)

        return graphs[0]

    def find_edge(self, v_a, v_b):
        if self.EDGE_CLS == UndirectedEdge:
            return next(edge for edge in self.edges if edge.vertex_pair == {v_a, v_b})
        elif self.EDGE_CLS == DirectedEdge:
            return next(edge for edge in self.edges if edge.from_vertex == v_a and edge.to_vertex == v_b)
        raise NotImplementedError

    def find_all_path(self, start_vertex_name, end_vertex_name):
        start_vertex = self.get_vertex_by_name(start_vertex_name)
        end_vertex = self.get_vertex_by_name(end_vertex_name)

        adj_dict = self.adjacency_dict

        def all_path(start, end, path=[]):

            path = path + [start]

            if (start == end):
                return [path]
            if start in adj_dict[start]:
                return None
            paths = []
            for vertex in adj_dict[start]:
                if vertex not in path:
                    new_paths = all_path(vertex, end, path)
                    for new_path in new_paths:
                        paths.append(new_path)
            return paths

        return all_path(start_vertex, end_vertex)

    def find_shortest_path(self, start_vertex_name, end_vertex_name):
        start_vertex = self.get_vertex_by_name(start_vertex_name)
        end_vertex = self.get_vertex_by_name(end_vertex_name)

        adj_dict = self.adjacency_dict

        def shortest_path(start, end, path=[]):
            path = path + [start]
            if start == end:
                return path
            if start not in self.vertexes:
                return None
            shortest = None
            for node in adj_dict[start]:
                if node not in path:
                    new_path = shortest_path(node, end, path)
                    if new_path:
                        if not shortest or len(new_path) < len(shortest):
                            shortest = new_path
            return shortest

        return shortest_path(start_vertex, end_vertex)

    def get_path_index_weight_dict(self, paths):
        path_weight_sum_dict = {path_index: 0 for path_index in range(len(paths))}
        for i, path in enumerate(paths):
            last_v = None
            path = path.copy()
            while path:
                v1 = path.pop(0)
                if last_v is None:
                    v2 = path.pop(0)
                    edge = self.find_edge(v1, v2)
                    last_v = v2
                else:
                    edge = self.find_edge(last_v, v1)
                    last_v = v1

                path_weight_sum_dict[i] += edge.weight

        return path_weight_sum_dict

    def find_shortest_paths_with_weight(self, start_vertex_name, end_vertex_name):
        all_paths = self.find_all_path(start_vertex_name, end_vertex_name)
        path_weight_sum_dict = self.get_path_index_weight_dict(all_paths)
        min_weight = min(path_weight_sum_dict.values())

        return [all_paths[path_index] for path_index, weight in path_weight_sum_dict.items() if
                weight == min_weight], min_weight

    def find_longest_path_with_weight(self, start_vertex_name, end_vertex_name):
        all_paths = self.find_all_path(start_vertex_name, end_vertex_name)
        path_weight_sum_dict = self.get_path_index_weight_dict(all_paths)
        if not path_weight_sum_dict:
            return [], 0

        max_weight = max(path_weight_sum_dict.values())

        return [all_paths[path_index] for path_index, weight in path_weight_sum_dict.items() if
                weight == max_weight], max_weight

    def find_critical_paths(self):
        max_weight = None
        critical_paths = None
        for v_a in self.vertexes:
            for v_b in self.vertexes:
                if v_a is not v_b:
                    *paths, weight = self.find_longest_path_with_weight(v_a.name, v_b.name)
                    if max_weight is None:
                        max_weight = weight
                        critical_paths = paths[0]
                    elif weight > max_weight:
                        max_weight = weight
                        critical_paths = paths[0]

        return critical_paths


class DirectedBase(Graph):
    EDGE_CLS = DirectedEdge

    def topological_sort(self):
        # 构建顶点入度字典
        ret_list = []
        reversed_adjacency_dict = self.reversed_adjacency_dict

        while 0 in [len(val) for val in
                    {v: d for v, d in reversed_adjacency_dict.items() if v not in ret_list}.values()]:
            for vertex, adjacency_vertexes in reversed_adjacency_dict.items():
                if len(adjacency_vertexes) == 0 and vertex not in ret_list:
                    ret_list.append(vertex)
                    for vs in reversed_adjacency_dict.values():
                        if vertex in vs:
                            vs.pop(vs.index(vertex))

        if len(ret_list) < len(self.vertexes):
            raise RuntimeError("有向图中存在环，无法进行拓扑排序")

        return ret_list


class DirectedGraph(DirectedBase):
    """有向图"""
    EDGE_CLS = DirectedEdge


class UndirectedGraph(Graph):
    """无向图"""
    EDGE_CLS = UndirectedEdge


class DirectedNetwork(DirectedBase):
    """有向网"""
    EDGE_CLS = DirectedEdge
    # 默认表示不可达的邻接矩阵最大元素值
    DEFAULT_UNREACHABLE_MAX_VALUE = -1

    def add_new_edge(self, from_vertex_name, to_vertex_name, weight=None):
        # 对于边权小于默认表示不可达的邻接矩阵最大元素值的，禁止该边的添加
        if weight and weight <= self.DEFAULT_UNREACHABLE_MAX_VALUE:
            raise exceptions.EdgeWeightError(f"有向网的边权不允许小于或等于{self.DEFAULT_UNREACHABLE_MAX_VALUE}")
        super().add_new_edge(from_vertex_name, to_vertex_name, weight)

    def add_edge(self, edge):
        if edge.weight and edge.weight <= self.DEFAULT_UNREACHABLE_MAX_VALUE:
            raise exceptions.EdgeWeightError(f"有向网的边权不允许小于或等于{self.DEFAULT_UNREACHABLE_MAX_VALUE}")
        super().add_edge(edge)


class UndirectedNetwork(Graph):
    """无向网"""
    EDGE_CLS = UndirectedEdge
    # 默认表示不可达的邻接矩阵最大元素值
    DEFAULT_UNREACHABLE_MAX_VALUE = -1

    def add_new_edge(self, from_vertex_name, to_vertex_name, weight=None):
        # 对于边权小于默认表示不可达的邻接矩阵最大元素值的，禁止该边的添加
        if weight and weight <= self.DEFAULT_UNREACHABLE_MAX_VALUE:
            raise exceptions.EdgeWeightError(f"无向网的边权不允许小于或等于{self.DEFAULT_UNREACHABLE_MAX_VALUE}")
        super().add_new_edge(from_vertex_name, to_vertex_name, weight)

    def add_edge(self, edge):
        if edge.weight and edge.weight <= self.DEFAULT_UNREACHABLE_MAX_VALUE:
            raise exceptions.EdgeWeightError(f"无向网的边权不允许小于或等于{self.DEFAULT_UNREACHABLE_MAX_VALUE}")
        super().add_edge(edge)
