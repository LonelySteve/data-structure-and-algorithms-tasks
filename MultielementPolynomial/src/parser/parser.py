from MultielementPolynomial.src.parser import nodes
from MultielementPolynomial.src.parser.nodes import MPExpression
from MultielementPolynomial.src.parser.lexer import Lexer, describe_token
from MultielementPolynomial.src.parser.exceptions import ExpressionSyntaxError

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
        raise ExpressionSyntaxError(f"{msg} at pos {pos}")

    def parse(self):
        result = self.parse_math1()
        if self.stream.current.type != 'eof':
            self.fail("unexpected '%s'" % describe_token(self.stream.current))
        return MPExpression(result)

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
            next(self.stream)  # 吞掉负号

            if self.stream.current.test("number"):
                node = nodes.Number(-self.stream.current.value)
                next(self.stream)
            elif self.stream.current.test("var"):
                # 对于变元前的负号，将转换为-1数字，例如 -x 将解析为 -1*x
                num = nodes.Number(-1)
                node = nodes.Mul(num, nodes.Variable(self.stream.current.value))
                next(self.stream)
            elif self.stream.current.test("lparen"):
                # 对于括弧前的负号，将转换为-1数字，例如 -(1-2) 将解析为 -1*(1-2)
                next(self.stream)  # 吞掉左括弧
                expr_node = self.parse_math1()
                node = nodes.Mul(nodes.Number(-1), expr_node)
                self.stream.expect("rparen")
            else:
                self.fail("unexpected '%s'" % describe_token(token))
        elif token_type == 'add':
            next(self.stream)

            if self.stream.current.test("number"):
                node = nodes.Number(self.stream.current.value)
                next(self.stream)
            elif self.stream.current.test("var"):
                node = nodes.Variable(self.stream.current.value)
                next(self.stream)
            elif self.stream.current.test("lparen"):
                next(self.stream)  # 吞掉左括弧
                expr_node = self.parse_math1()
                node = expr_node
                self.stream.expect("rparen")
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
            node = self.parse_math1()
            self.stream.expect('rparen')
        else:
            self.fail("unexpected '%s'" % describe_token(token), token.pos)

        return node


if __name__ == '__main__':
    p = Parser("123 * 12 * 456 + 123")
    print(p.parse())
