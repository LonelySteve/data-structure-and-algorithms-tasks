import pytest
from graph import DirectedGraph, UndirectedGraph, DirectedNetwork, UndirectedNetwork, Vertex as vt
import exceptions


class TestUndirectedGraph(object):
    def test_create(self):
        ug = UndirectedGraph("A", "B", "C")
        ug.add_new_edge("A", "B")
        ug.add_new_edge("B", "C")

        assert [v.name for v in ug.vertexes] == ["A", "B", "C"]
        assert ug.adjacency_dict == {
            vt("A"): [vt("B")],
            vt("B"): [vt("A"), vt("C")],
            vt("C"): [vt("B")]
        }

        with pytest.raises(exceptions.VertexNotExistError):
            ug.get_vertex_by_name("E")

        with pytest.raises(exceptions.VertexNotExistError):
            ug.add_new_edge("C", "E")

    def test_traverse(self):
        vertexes_names = []

        def traverse_visit_callback(vertex):
            vertexes_names.append(vertex.name)

        un = UndirectedGraph("A", "B", "C", "D")
        un.add_new_edge("A", "B")
        un.add_new_edge("B", "C")
        un.add_new_edge("C", "D")

        # bfs
        un.bfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]
        vertexes_names = []
        # dfs
        un.dfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]

    def test_find_shortest_path(self):
        dg = UndirectedGraph("A", "B", "C", "D")
        dg.add_new_edge("A", "B")
        dg.add_new_edge("B", "D")
        dg.add_new_edge("B", "C")
        dg.add_new_edge("A", "C")
        dg.add_new_edge("C", "D")
        result = dg.find_shortest_path("A", "D")
        assert result == [vt("A"), vt("B"), vt("D")] or result == [vt("A"), vt("C"), vt("D")]


class TestDirectedGraph(object):

    def test_create(self):
        dg = DirectedGraph()
        dg.extend_vertexes("A", "B", "C", "D")
        dg.add_new_edge("A", "B")
        dg.add_new_edge("B", "C")
        dg.add_new_edge("C", "D")
        assert [v.name for v in dg.vertexes] == ["A", "B", "C", "D"]
        assert dg.adjacency_dict == {
            vt("A"): [vt("B")],
            vt("B"): [vt("C")],
            vt("C"): [vt("D")],
            vt("D"): [],
        }

        with pytest.raises(exceptions.VertexNotExistError):
            dg.get_vertex_by_name("E")

        with pytest.raises(exceptions.VertexNotExistError):
            dg.add_new_edge("E", "B")

    def test_traverse(self):
        vertexes_names = []

        def traverse_visit_callback(vertex):
            vertexes_names.append(vertex.name)

        dg = DirectedGraph("A", "B", "C", "D")
        dg.add_new_edge("A", "B")
        dg.add_new_edge("B", "C")
        dg.add_new_edge("C", "D")

        # bfs
        dg.bfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]
        vertexes_names = []
        # dfs
        dg.dfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]

    def test_topological_sort(self):
        dg = DirectedGraph()
        dg.extend_vertexes("A", "B", "C", "D")
        dg.add_new_edge("A", "B")
        dg.add_new_edge("B", "C")
        dg.add_new_edge("C", "D")

        assert dg.topological_sort() == [vt("A"), vt("B"), vt("C"), vt("D")]

        dg = DirectedGraph("A", "B", "C")
        dg.add_new_edge("A", "B")
        dg.add_new_edge("B", "C")
        dg.add_new_edge("C", "A")

        with pytest.raises(RuntimeError, match="存在环"):
            dg.topological_sort()

        dg = DirectedGraph("A", "B", "C", "D")
        dg.add_new_edge("A", "B")
        dg.add_new_edge("A", "D")
        dg.add_new_edge("B", "C")
        dg.add_new_edge("D", "C")

        result = dg.topological_sort()
        assert result == [vt("A"), vt("B"), vt("D"), vt("C")] or result == [vt("A"), vt("D"), vt("B"), vt("C")]


class TestUndirectedNetwork(object):
    def test_create(self):
        un = UndirectedNetwork("A", "B", "C")
        un.add_new_edge("A", "B", 1.5)
        un.add_new_edge("B", "C", 7)
        assert [v.name for v in un.vertexes] == ["A", "B", "C"]

        assert un.adjacency_dict == {
            vt("A"): [vt("B")],
            vt("B"): [vt("A"), vt("C")],
            vt("C"): [vt("B")]
        }

        with pytest.raises(exceptions.VertexNotExistError):
            un.get_vertex_by_name("E")

        with pytest.raises(exceptions.VertexNotExistError):
            un.add_new_edge("E", "B")

    def test_traverse(self):
        vertexes_names = []

        def traverse_visit_callback(vertex):
            vertexes_names.append(vertex.name)

        un = UndirectedNetwork("A", "B", "C", "D")
        un.add_new_edge("A", "B")
        un.add_new_edge("B", "C")
        un.add_new_edge("C", "D")

        # bfs
        un.bfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]
        vertexes_names = []
        # dfs
        un.dfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]

    def test_get_minimum_spanning_tree(self):
        un = UndirectedNetwork("A", "B", "C", "D", "E", "F")
        un.add_new_edge("A", "B", 6)
        un.add_new_edge("B", "E", 3)
        un.add_new_edge("E", "F", 6)
        un.add_new_edge("F", "D", 2)
        un.add_new_edge("D", "A", 5)
        un.add_new_edge("A", "C", 1)
        un.add_new_edge("B", "C", 5)
        un.add_new_edge("E", "C", 6)
        un.add_new_edge("F", "C", 4)
        un.add_new_edge("D", "C", 5)
        tree = un.get_minimum_spanning_tree()
        assert tree.adjacency_dict == {
            vt("A"): [vt("C")],
            vt("B"): [vt("E"), vt("C")],
            vt("C"): [vt("A"), vt("F"), vt("B")],
            vt("D"): [vt("F")],
            vt("E"): [vt("B")],
            vt("F"): [vt("D"), vt("C")]
        }

    def test_find_shortest_paths(self):
        un = UndirectedNetwork("A", "B", "C", "D")
        un.add_new_edge("A", "B", 1)
        un.add_new_edge("B", "D", 3)
        un.add_new_edge("B", "C", 1)
        un.add_new_edge("A", "C", 3)
        un.add_new_edge("C", "D", 1)
        assert un.find_shortest_paths_with_weight("A", "D")[0][0] == [vt("A"), vt("B"), vt("C"), vt("D")]

    def test_find_critical_paths(self):
        un = UndirectedNetwork("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9")
        un.add_new_edge("V1", "V2", 6)
        un.add_new_edge("V2", "V5", 1)
        un.add_new_edge("V5", "V7", 9)
        un.add_new_edge("V7", "V9", 2)
        un.add_new_edge("V1", "V3", 4)
        un.add_new_edge("V3", "V5", 1)
        un.add_new_edge("V5", "V8", 7)
        un.add_new_edge("V8", "V9", 4)
        un.add_new_edge("V1", "V4", 5)
        un.add_new_edge("V4", "V6", 2)
        un.add_new_edge("V6", "V8", 4)

        result = un.find_critical_paths()

        assert len(result) == 1
        assert [vt("V2"), vt("V1"), vt("V4"), vt("V6"), vt("V8"), vt("V5"), vt("V7"), vt("V9")] in result


class TestDirectedNetwork(object):
    def test_create(self):
        dn = DirectedNetwork()
        dn.extend_vertexes("A", "B", "C", "D")
        dn.add_new_edge("A", "B")
        dn.add_new_edge("B", "C")
        dn.add_new_edge("C", "D")
        assert [v.name for v in dn.vertexes] == ["A", "B", "C", "D"]
        assert dn.adjacency_dict == {
            vt("A"): [vt("B")],
            vt("B"): [vt("C")],
            vt("C"): [vt("D")],
            vt("D"): [],
        }

        with pytest.raises(exceptions.VertexNotExistError):
            dn.get_vertex_by_name("E")

        with pytest.raises(exceptions.VertexNotExistError):
            dn.add_new_edge("E", "B")

    def test_topological_sort(self):
        dn = DirectedNetwork()
        dn.extend_vertexes("A", "B", "C", "D")
        dn.add_new_edge("A", "B")
        dn.add_new_edge("B", "C")
        dn.add_new_edge("C", "D")

        assert dn.topological_sort() == [vt("A"), vt("B"), vt("C"), vt("D")]

        dn = DirectedNetwork("A", "B", "C")
        dn.add_new_edge("A", "B")
        dn.add_new_edge("B", "C")
        dn.add_new_edge("C", "A")

        with pytest.raises(RuntimeError, match="存在环"):
            dn.topological_sort()

        dn = DirectedNetwork("A", "B", "C", "D")
        dn.add_new_edge("A", "B")
        dn.add_new_edge("A", "D")
        dn.add_new_edge("B", "C")
        dn.add_new_edge("D", "C")

        assert dn.topological_sort() == [vt("A"), vt("B"), vt("D"), vt("C")] or [vt("A"), vt("D"), vt("B"), vt("C")]

    def test_traverse(self):
        vertexes_names = []

        def traverse_visit_callback(vertex):
            vertexes_names.append(vertex.name)

        dn = DirectedNetwork("A", "B", "C", "D")
        dn.add_new_edge("A", "B")
        dn.add_new_edge("B", "C")
        dn.add_new_edge("C", "D")

        # bfs
        dn.bfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]
        vertexes_names = []
        # dfs
        dn.dfs_traverse("A", traverse_visit_callback)
        assert vertexes_names == ["A", "B", "C", "D"]

    def test_get_minimum_spanning_tree(self):
        dn = DirectedNetwork("A", "B", "C", "D")
        dn.add_new_edge("A", "B", 5)
        dn.add_new_edge("B", "D", 3)
        dn.add_new_edge("C", "B", 2)
        dn.add_new_edge("A", "C", 1)
        dn.add_new_edge("D", "C", 4)

        tree = dn.get_minimum_spanning_tree()
        assert tree.adjacency_dict == {
            vt("A"): [vt("C")],
            vt("B"): [vt("D")],
            vt("C"): [vt("B")],
            vt("D"): [],
        }

    def test_find_critical_paths(self):
        un = DirectedNetwork("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9")
        un.add_new_edge("V1", "V2", 6)
        un.add_new_edge("V2", "V5", 1)
        un.add_new_edge("V5", "V7", 9)
        un.add_new_edge("V7", "V9", 2)
        un.add_new_edge("V1", "V3", 4)
        un.add_new_edge("V3", "V5", 1)
        un.add_new_edge("V5", "V8", 7)
        un.add_new_edge("V8", "V9", 4)
        un.add_new_edge("V1", "V4", 5)
        un.add_new_edge("V4", "V6", 2)
        un.add_new_edge("V6", "V8", 4)

        result = un.find_critical_paths()

        assert len(result) == 2
        assert [vt("V1"), vt("V2"), vt("V5"), vt("V7"), vt("V9")] in result
        assert [vt("V1"), vt("V2"), vt("V5"), vt("V8"), vt("V9")] in result
