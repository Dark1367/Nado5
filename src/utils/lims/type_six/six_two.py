from src.utils.Random import Random
import os

async def fmt_exp(exp):
    if exp == 0:
        return "n"
    elif exp > 0:
        return f"n+{exp}"
    else:
        return f"n{exp}"

async def fmt_term(coef, base, exp):
    exp_str = await fmt_exp(exp)
    
    if coef == 1:
        return f"{base}^{{{exp_str}}}"
    elif coef == -1:
        return f"-{base}^{{{exp_str}}}"
    else:
        return f"{coef} \\cdot {base}^{{{exp_str}}}"

async def generate_limit(rand):
    bases = [2, 3, 4, 5, 6, 7, 8, 9]
    b_num = bases[rand.randint(0, len(bases)-1)]
    
    if rand.randint(0, 1) == 0:
        b_den1 = bases[rand.randint(0, len(bases)-1)]
        b_den2 = bases[rand.randint(0, len(bases)-1)]
        while b_den2 == b_den1:
            b_den2 = bases[rand.randint(0, len(bases)-1)]
    else:
        b_den1 = bases[rand.randint(0, len(bases)-1)]
        b_den2 = b_den1
    
    c_num = rand.randint(-8, 8)
    while c_num == 0:
        c_num = rand.randint(-8, 8)
    
    c_den1 = rand.randint(-8, 8)
    while c_den1 == 0:
        c_den1 = rand.randint(-8, 8)
    
    c_den2 = rand.randint(-8, 8)
    while c_den2 == 0:
        c_den2 = rand.randint(-8, 8)
    
    s_num = rand.randint(-4, 4)
    s_den1 = rand.randint(-4, 4)
    s_den2 = rand.randint(-4, 4)
    numerator = await fmt_term(c_num, b_num, s_num)
    denom1 = await fmt_term(c_den1, b_den1, s_den1)
    denom2 = await fmt_term(c_den2, b_den2, s_den2)
    
    if denom2.startswith('-'):
        denominator = denom1 + denom2
    else:
        denominator = denom1 + " + " + denom2
    
    if denominator.startswith('+'):
        denominator = denominator[1:]
    
    primer = f"\\lim_{{n \\to \\infty}} \\frac{{{numerator}}}{{{denominator}}}"
    return primer

async def generate_lim_6_2(rand, n):
    primer = []
    for _ in range(n):
        primer.append(await generate_limit(rand))
    return primer