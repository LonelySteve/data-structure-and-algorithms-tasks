from MultielementPolynomial.src.parser.parser import Parser



def test_1():
    p = Parser("123+456")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "579"

def test_2():
    p = Parser("123-456")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "-333"

def test_3():
    p = Parser("1+2*3")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "7"

def test_4():
    p = Parser("9-8*1")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "1"

def test_5():
    p = Parser("9-9*1")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "0"

def test_6():
    p = Parser("9-9*(2-3^6)")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "6552"

def test_7():
    p = Parser("x")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "x"

def test_8():
    p = Parser("x*x^2*x^3")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "x^6"

def test_9():
    p = Parser("x*(x^2+x^3)")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "x^3+x^4"

def test_10():
    p = Parser("(8*x^9+5*x^8*y^7+3*x^4*y^4+6*y^2-5) * (6*x^5*y^4+7*x^3*y^2+21*x*y^2+8)")
    ex = p.parse()
    result = ex.get_value()
    assert str(result) == "48x^14*y^4+56x^12*y^2+168x^10*y^2+64x^9+30x^13*y^11" \
                          "+35x^11*y^9+105x^9*y^9+40x^8*y^7+18x^9*y^8+21x^7*y^6" \
                          "+99x^5*y^6+24x^4*y^4+42y^4*x^3+126y^4*x+48y^2-30x^5*y^4-35x^3*y^2-105x*y^2-40"
