from src.utils.Random import Random
import os

async def fmt_q(q):
    if q == int(q):
        return str(int(q))
    
    sign = "-" if q < 0 else ""
    abs_q = abs(q)

    for denom in range(2, 21):
        numer = round(abs_q * denom)
        if abs(abs_q - numer/denom) < 1e-10:
            if numer == denom:
                return f"{sign}1"
            a, b = numer, denom
            while b:
                a, b = b, a % b
            gcd = a
            numer //= gcd
            denom //= gcd
            if denom == 1:
                return f"{sign}{numer}"
            return f"{sign}\\frac{{{numer}}}{{{denom}}}"
    return str(round(q, 2))

async def simple(rand):
    a = rand.randint(1, 10) / 2
    while a == 1:
        a = rand.randint(1, 10) / 2
    
    b = rand.randint(1, 10) / 2
    while b == 1 or b == a:
        b = rand.randint(1, 10) / 2

    sa = await fmt_q(a)
    sb = await fmt_q(b)

    top = f"1 + {sa} + {sa}^2 + \\cdots + {sa}^n"
    bot = f"1 + {sb} + {sb}^2 + \\cdots + {sb}^n"

    res = f"\\lim_{{n \\to \\infty}} \\frac{{{top}}}{{{bot}}}"
    return res

async def with_offset(rand):
    off1 = rand.randint(0, 4)
    off2 = rand.randint(0, 4)
    a = rand.randint(1, 8) / 2
    while a == 1:
        a = rand.randint(1, 8) / 2
    b = rand.randint(1, 8) / 2
    while b == 1 or b == a:
        b = rand.randint(1, 8) / 2

    sa = await fmt_q(a)
    sb = await fmt_q(b)

    if off1 == 0:
        top = f"1 + {sa} + {sa}^2 + \\cdots + {sa}^n"
    else:
        top = f"{sa}^{{{off1}}}"
        for i in range(off1 + 1, off1 + 4):
            if i <= off1 + 3:
                top += f" + {sa}^{{{i}}}"
        top += f" + \\cdots + {sa}^{{n}}"

    if off2 == 0:
        bot = f"1 + {sb} + {sb}^2 + \\cdots + {sb}^n"
    else:
        bot = f"{sb}^{{{off2}}}"
        for i in range(off2 + 1, off2 + 4):
            if i <= off2 + 3:
                bot += f" + {sb}^{{{i}}}"
        bot += f" + \\cdots + {sb}^{{n}}"

    return f"\\lim_{{n \\to \\infty}} \\frac{{{top}}}{{{bot}}}"

async def with_coef(rand):
    k1 = rand.randint(1, 10)
    k2 = rand.randint(1, 10)
    a = rand.randint(1, 8) / 2
    while a == 1:
        a = rand.randint(1, 8) / 2
    b = rand.randint(1, 8) / 2
    while b == 1 or b == a:
        b = rand.randint(1, 8) / 2

    sa = await fmt_q(a)
    sb = await fmt_q(b)

    top = f"{k1}(1 + {sa} + {sa}^2 + \\cdots + {sa}^n)"
    bot = f"{k2}(1 + {sb} + {sb}^2 + \\cdots + {sb}^n)"

    return f"\\lim_{{n \\to \\infty}} \\frac{{{top}}}{{{bot}}}"

async def alternating(rand):
    a = rand.randint(1, 5) / 2
    while a == 1:
        a = rand.randint(1, 5) / 2
    s = await fmt_q(a)
    top = f"1 + {s} + {s}^2 + \\cdots + {s}^n"
    bot = f"1 + {s} + {s}^2 + {s}^3 + \\cdots + {s}^n"
    return f"\\lim_{{n \\to \\infty}} \\frac{{{top}}}{{{bot}}}"

async def generate_limit(rand):
    v = rand.randint(1, 4)

    if v == 1:
        return await simple(rand)
    elif v == 2:
        return await with_offset(rand)
    elif v == 3:
        return await with_coef(rand)
    elif v == 4:
        return await alternating(rand)

async def generate_lim_7_1(rand, n):
    primer = []
    for _ in range(n):
        primer.append(await generate_limit(rand))
    return primer
