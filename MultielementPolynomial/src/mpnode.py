class MPNode(object):
    def __init__(self, exp, coef=None, mplist=None, next=None):
        self.next = next
        self.exp = exp
        self.coef = coef
        self.mplist = mplist

    def __repr__(self):
        return f"({self.mplist or self.coef},{self.exp})"
