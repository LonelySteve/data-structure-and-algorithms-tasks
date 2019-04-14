from MultielementPolynomial.src.parser.parser import Parser
from MultielementPolynomial.src.mplist import get_mp_struct, convert


def main():
    expr_1 = "8*x^9+5*x^8*y^7+3*x^4*y^4+6*y^2-5"
    expr_2 = "6*x^5*y^4+7*x^3*y^2+21*x*y^2+8"

    p_1 = Parser(expr_1)
    ex_1 = p_1.parse()
    vars_1 = list(ex_1.vars)
    value_1 = ex_1.get_value()
    print(get_mp_struct(value_1, vars_1))

    p_2 = Parser(expr_2)
    ex_2 = p_2.parse()
    vars_2 = list(ex_2.vars)
    value_2 = ex_2.get_value()
    print(get_mp_struct(value_2, vars_2))

    mp_1 = convert(ex_1)
    mp_2 = convert(ex_2)
    print(mp_1 * mp_2)


if __name__ == '__main__':
    main()
