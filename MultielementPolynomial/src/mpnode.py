class MPNode(object):
    def __init__(self, exp, coef=None, mplist=None, next=None):
        self.next = next
        self.exp = exp
        self.coef = coef
        self.mplist = mplist

    def __mul__(self, other):
        if isinstance(other, MPNode):
            if self.mplist is not None and other.mplist is not None:
                return MPNode(self.exp + other.exp, mplist=self.mplist * other.mplist)
            elif self.coef is not None and other.coef is None:
                return MPNode(self.exp + other.exp, mplist=other.mplist * self.coef)
            elif other.coef is not None and self.coef is None:
                return MPNode(self.exp + other.exp, mplist=self.mplist * other.coef)
            else:
                return MPNode(self.exp + other.exp, coef=self.coef * other.coef)
        elif isinstance(other, (int, float)):
            if self.coef is None:
                return MPNode(self.exp, mplist=self.mplist * other)
            else:
                return MPNode(self.exp, coef=self.coef * other)
        else:
            raise ValueError("不支持与MPNode之外的节点相乘")

    def __repr__(self):
        return f"({self.mplist or self.coef},{self.exp})"
