import re
from collections import deque
from operator import itemgetter
import sys
from src.parser.exceptions import ExpressionSyntaxError

TOKEN_INITIAL = sys.intern("initial")
TOKEN_NUMBER = sys.intern("number")
TOKEN_VAR = sys.intern("var")
TOKEN_ADD = sys.intern('add')
TOKEN_SUB = sys.intern('sub')
TOKEN_MUL = sys.intern('mul')
TOKEN_POW = sys.intern('pow')
TOKEN_LPAREN = sys.intern('lparen')  # 左括弧
TOKEN_RPAREN = sys.intern('rparen')  # 右括弧
TOKEN_EOF = sys.intern("eof")

operators = {
    '+': TOKEN_ADD,
    '-': TOKEN_SUB,
    '*': TOKEN_MUL,
    '^': TOKEN_POW,
    '(': TOKEN_LPAREN,
    ')': TOKEN_RPAREN,
}

tok_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in [
    ('PAREN', r'[()]'),  # 匹配括弧
    ('NUMBER', r'\d+(\.\d*)?'),  # 整数和小数 (不含负号)
    ('VAR', r'[a-zA-Z]'),  # 变元
    ('OPERATOR', r'[\+\-\*^]'),  # 算数操作符
    ('SKIP', r'[ \t]+'),  # 空白和制表符
    ('MISMATCH', r'.'),  # 匹配任何其它字符
]))


def describe_token(token):
    if token.type == "var":
        return token.value
    return token.type


def describe_token_expr(expr):
    if ':' in expr:
        type, value = expr.split(':', 1)
        if type == "var":
            return value
    else:
        type = expr

    if type in operators:
        return operators[type]

    return type


class Token(tuple):
    """Token class."""
    __slots__ = ()
    type, value, pos = (property(itemgetter(x)) for x in range(3))

    def __new__(cls, type, value, pos):
        return tuple.__new__(cls, (sys.intern(str(type)), value, pos))

    def __str__(self):
        if self.type in operators:
            return operators[self.type]
        elif self.type == 'name':
            return self.value
        return self.type

    def test(self, expr):
        """Test a token against a token expression.  This can either be a
        token type or ``'token_type:token_value'``.  This can only test
        against string values and types.
        """
        # here we do a regular string equality check as test_any is usually
        # passed an iterable of not interned strings.
        if self.type == expr:
            return True
        elif ':' in expr:
            return expr.split(':', 1) == [self.type, self.value]
        return False

    def test_any(self, *iterable):
        """Test against multiple token expressions."""
        for expr in iterable:
            if self.test(expr):
                return True
        return False

    def __repr__(self):
        return 'Token(%r, %r, %r)' % (
            self.type,
            self.value,
            self.pos
        )


class TokenStreamIterator(object):
    """The iterator for tokenstreams.  Iterate over the stream
    until the eof token is reached.
    """

    def __init__(self, stream):
        self.stream = stream

    def __iter__(self):
        return self

    def __next__(self):
        token = self.stream.current
        if token.type is TOKEN_EOF:
            self.stream.close()
            raise StopIteration()
        next(self.stream)
        return token


class TokenStream(object):
    """A token stream is an iterable that yields :class:`Token`\\s.  The
    parser however does not iterate over it but calls :meth:`next` to go
    one token ahead.  The current active token is stored as :attr:`current`.
    """

    def __init__(self, generator):
        self._iter = iter(generator)
        self._buffer_deque = deque()

        self.closed = False
        self.current = Token(1, TOKEN_INITIAL, '')
        next(self)

    def __iter__(self):
        return TokenStreamIterator(self)

    def __bool__(self):
        return bool(self._buffer_deque) or self.current.type is not TOKEN_EOF

    def __next__(self):
        """Go one token ahead and return the old one.

        Use the built-in :func:`next` instead of calling this directly.
        """
        rv = self.current
        # 这里的队列起到了临时缓存的作用，当队列中有token时优先弹出队列的token
        # 否则再尝试迭代出迭代器中的token
        if self._buffer_deque:
            self.current = self._buffer_deque.popleft()
        elif self.current.type is not TOKEN_EOF:
            try:
                self.current = next(self._iter)
            except StopIteration:
                self.close()
        return rv

    def close(self):
        """Close the stream."""
        self.current = Token(TOKEN_EOF, '', self.current.pos)
        self._iter = None
        self.closed = True

    def push(self, token):
        """Push a token back to the stream."""
        self._buffer_deque.append(token)

    def look(self):
        """Look at the next token."""
        old_token = next(self)
        result = self.current
        self.push(result)
        self.current = old_token
        return result

    def skip(self, n=1):
        """Got n tokens ahead."""
        for x in range(n):
            next(self)

    def next_if(self, expr):
        """Perform the token test and return the token if it matched.
        Otherwise the return value is `None`.
        """
        if self.current.test(expr):
            return next(self)

    def skip_if(self, expr):
        """Like :meth:`next_if` but only returns `True` or `False`."""
        return self.next_if(expr) is not None

    def expect(self, expr):
        """Expect a given token type and return it.  This accepts the same
        argument as :meth:`jinja2.lexer.Token.test`.
        """
        if not self.current.test(expr):
            expr = describe_token_expr(expr)
            if self.current.type is TOKEN_EOF:
                raise ExpressionSyntaxError('unexpected end of expression, '
                                            'expected %r.' % expr,
                                            self.current.pos,
                                            )
            raise ExpressionSyntaxError("expected token %r, got %r" %
                                        (expr, describe_token(self.current)),
                                        self.current.pos)
        try:
            return self.current
        finally:
            next(self)


class Lexer(object):

    def tokenize(self, code):
        return TokenStream(self.wrap(self.tokeniter(code)))

    def wrap(self, stream):
        for kind, value, pos in stream:
            if kind == "NUMBER":
                kind = 'number'
            elif kind == "PAREN" or kind == "OPERATOR":
                kind = operators.get(value)
            elif kind == "VAR":
                kind = 'var'
            yield Token(kind, value, pos)

    def tokeniter(self, code):
        pos_start = 0
        pos = 0
        # 括弧平衡栈
        balancing_stack = []
        for mo in tok_regex.finditer(code):
            kind = mo.lastgroup
            value = mo.group()
            pos = mo.start() - pos_start
            if kind == "SKIP":
                # 跳过所有空白符
                continue
            elif kind == "NUMBER":
                # 转换值类型
                value = float(value) if '.' in value else int(value)
            elif kind == "PAREN":
                if value == '(':
                    balancing_stack.append(')')
                elif value in [')']:
                    if not balancing_stack:
                        raise ExpressionSyntaxError(f'{value!r} unexpected on pos {pos}')
                    expected_op = balancing_stack.pop()
                    if expected_op != value:
                        raise ExpressionSyntaxError(f'{value!r} unexpected on pos {pos}, excepted {expected_op!r}')
            elif kind == "MISMATCH":
                # 不支持识别的字符或字符串直接抛出错误
                raise ExpressionSyntaxError(f'{value!r} unexpected on pos {pos}')
            yield kind, value, pos
        if balancing_stack:
            raise ExpressionSyntaxError(f'expected {balancing_stack[0]!r} on pos {pos}')

if __name__ == '__main__':
    p = Lexer()
    for token in p.tokenize("xy - (x + 2)"):
        print(token)
