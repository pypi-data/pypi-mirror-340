def resh(y=''):
    x = 0
    import math
    zero = len(y) - 1
    x_in_1 = y.rfind('x')
    x_in_2 = y.find('x')

    if y.find('-', 0, x_in_2) == -1:  # фигня для поиска а
        kol_a = 1
        kola = 0
        a = y[kola]
        for i in range(1, x_in_2):
            a += y[kol_a]
            kol_a += 1
        a = int(a)
    else:
        kol_a = 3
        kola = 2
        a = y[kola]
        for i in range(3, x_in_2):
            a += y[kol_a]
            kol_a += 1
        a = (-1) * int(a)

    if y.find('-', x_in_2, x_in_1) == -1:  # фигня для поиска b
        kol_b = x_in_2 + 7
        kolb = x_in_2 + 6
        b = y[kolb]
        for i in range(x_in_2 + 7, x_in_1):
            b += y[kol_b]
            kol_b += 1
        b = int(b)
    else:
        kol_b = x_in_2 + 7
        kolb = x_in_2 + 6
        b = y[kolb]
        for i in range(x_in_2 + 7, x_in_1):
            b += y[kol_b]
            kol_b += 1
        b = (-1) * int(b)

    if y.find('-', x_in_1, y.find('=')) == -1:  # фигня для поиска c
        kol_c = x_in_1 + 4
        kolc = x_in_1 + 3
        c = y[kolc]
        for i in range(x_in_1 + 3, y.find('=') - 1):
            c += y[kol_c]
            kol_c += 1
        c = int(c)
    else:
        kol_c = x_in_1 + 4
        kolc = x_in_1 + 3
        c = y[kolc]
        for i in range(x_in_1 + 3, y.find('=') - 1):
            c += y[kol_c]
            kol_c += 1
        c = (-1) * int(c)
    D = (b * b) - (4 * a * c)
    if D > 0:
        d = (math.sqrt(D))
    if D > 0:
        return ('x1 =', (((-1) * b) - d) / (2 * a), 'x2 =', (((-1) * b) + d) / (2 * a))
    elif D == 0:
        return ('x =', ((-1) * b) / (2 * a))
    else:
        return ('Корней нет(((')
