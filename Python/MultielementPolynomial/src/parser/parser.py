from src.parser import nodes
from src.parser.lexer import Lexer, describe_token
from src.parser.exceptions import ExpressionSyntaxError

_math_nodes = {
    'add': nodes.Add,
    'sub': nodes.Sub,
    'mul': nodes.Mul,
    'pow': nodes.Pow,
}


class Parser(object):

    def __init__(self, code):
        self.stream = Lexer().tokenize(code)

    def fail(self, msg, pos=None):
        """Convenience method that raises `exc` with the message, passed
        line number or last line number as well as the current name and
        filename.
        """
        if pos is None:
            pos = self.stream.current.pos
        raise ExpressionSyntaxError(msg + " at pos " + pos)

    def parse(self):
        return self.parse_math1()

    def parse_math1(self):
        left = self.parse_math2()
        while self.stream.current.type in ('add', 'sub'):
            node_cls = _math_nodes[self.stream.current.type]
            next(self.stream)
            right = self.parse_math2()
            left = node_cls(left, right)
        return left

    def parse_math2(self):
        left = self.parse_pow()
        while self.stream.current.type in ('mul'):
            cls = _math_nodes[self.stream.current.type]
            next(self.stream)
            right = self.parse_pow()
            left = cls(left, right)
        return left

    def parse_pow(self):
        left = self.parse_unary()
        while self.stream.current.type in ('pow'):
            cls = _math_nodes[self.stream.current.type]
            next(self.stream)
            right = self.parse_unary()
            left = cls(left, right)
        return left

    def parse_unary(self):
        token = self.stream.current
        token_type = token.type
        if token_type == 'sub':
            next(self.stream)
            num = self.stream.next_if("number")
            if num:
                node = nodes.Number(-num.value)
            else:
                var = self.stream.next_if("var")
                if var:
                    coef = nodes.Number(-1)
                    var = nodes.Variable(var.value)
                    node = nodes.Mul(coef, var)
                else:
                    self.fail("unexpected '%s'" % describe_token(token))

        elif token_type == 'add':
            next(self.stream)
            num = self.stream.next_if("number")
            if num:
                node = nodes.Number(num.value)
            else:
                var = self.stream.next_if("var")
                if var:
                    coef = nodes.Number(1)
                    var = nodes.Variable(var.value)
                    node = nodes.Mul(coef, var)
                else:
                    self.fail("unexpected '%s'" % describe_token(token))
        else:
            node = self.parse_primary()

        return node

    def parse_primary(self):
        token = self.stream.current
        if token.type == 'var':
            node = nodes.Variable(token.value)
            next(self.stream)
        elif token.type in ('number'):
            node = nodes.Number(token.value)
            next(self.stream)
        elif token.type == 'lparen':
            next(self.stream)
            node = self.parse()
            self.stream.expect('rparen')
        else:
            self.fail("unexpected '%s'" % describe_token(token), token.pos)

        return node


if __name__ == '__main__':
    p = Parser("2* x * y ^ 2 - (x + 2)")
    print(p.parse())
