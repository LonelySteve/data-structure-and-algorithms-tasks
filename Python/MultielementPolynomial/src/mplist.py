class MPList(object):
    def __init__(self, var):
        self.head = None
        self.tail = None
        self.var = var

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

    def __repr__(self):
        return f"{self.var}({', '.join([node for node in self])})"
