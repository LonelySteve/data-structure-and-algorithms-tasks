from MultielementPolynomial.src.parser.parser import Parser


def mainloop():
    try:
        while True:
            mp = input("MP>")
            mp = mp.strip()
            if mp:
                p = Parser(mp)
                ex = p.parse()
                print(ex.get_value())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    print("多元多项式计算器 by JLoeve")
    print("========================")
    print("可支持加法，减法，乘法以及子表达式")
    mainloop()
