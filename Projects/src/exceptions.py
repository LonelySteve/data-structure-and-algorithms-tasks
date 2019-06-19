class VertexError(Exception):
    """顶点相关错误"""


class VertexTypeError(VertexError):
    """顶点类型错误"""


class NetworkError(Exception):
    """网异常"""


class CannotConnectNetworkError(NetworkError):
    """试图将两个网络合并时产生的异常"""


class RepeatVertexesError(VertexError):
    """同一网络下顶点重复导致的异常"""


class VertexDifferentNetworkError(VertexError):
    """试图将两个处于不同网络的顶点相连导致的异常"""


class MatrixRankError(Exception):
    """矩阵秩错误"""


class VertexNotExistError(VertexError):
    """顶点不存在错误"""


class EdgeTypeError(Exception):
    """边类型错误"""


class EdgeWeightError(Exception):
    """边权错误"""
